# Journey

This page is to document the journey of developing this project.

## Topics

### macOS Verbose Logs

- Machine: macOS M1 Pro Max 2021 (arm64)
- OS: Sonoma 14.2
- Xcode Version: 15.1
- Audacity Version: 3.4.2

The tests pass on both macOS and Windows, though on macOS, the output is verbose and noisy; here's an example:

```
Server received Select: Start=0.0 End=1.35637 Track=2.0
Server sending
Server sending BatchCommand finished: OK
Server sending
Read failed on fifo, quitting
Server received Paste:
Server sending
Server sending BatchCommand finished: OK
Server sending
Read failed on fifo, quitting
Server received Select: Start=1.8005 End=2.41111 Track=0.0
Server sending
Server sending BatchCommand finished: OK
Server sending
Read failed on fifo, quitting
```

#### The GoLang Pipe

Initially, I thought it might be cool to create a GoLang package that would handle the pipes; I used [gopy](https://github.com/go-python/gopy) to compile and build the library to consume it in Python as `audacity_pipe.so` file. A POC of this attempt was done on this branch [feature/pipe-golang-lib](https://github.com/unfor19/audacity-scripting/tree/feature/pipe-golang-lib). And even after using this custom pipe library, the macOS logs kept shooting like crazy.

#### Look At The Source

Well, Audacity is an open-source available on [GitHub](https://github.com/audacity/audacity), so why not just search for `Server sending` and `Read failed on fifo, quitting` in Audacity's code ... So I did and found this - [Audacity 3.4.2 - modules/mod-script-pipe/PipeServer.cpp#L187](https://github.com/audacity/audacity/blob/release-3.4.2/modules/mod-script-pipe/PipeServer.cpp#L187)

```cpp
    //  .....
         printf("Server sending %s",buf);

         // len - 1 because we do not send the null character
         fwrite(buf, 1, len - 1, fromFifo);
      }
      fflush(fromFifo);
   }

   printf("Read failed on fifo, quitting\n");
```

So I thought, why not build Audacity locally on my machine, remove those `printf` functions, and hopefully, we'll have clean logs, just like Windows? It's important to note that the `PipeServer.cpp` file has a different setting for Windows and non-Windows (Unix/macOS).

#### Building Audacity From Source

Surprisingly, it was super easy to build Audacity locally. I followed the instructions on this page, [Audacity BUILDING.md](https://github.com/audacity/audacity/blob/53f3200d278bed6862ca2bebc5416fe8cbe1d348/BUILDING.md).

My only issue was with Conan, where I needed to install it globally on my machine before running the build commands. I already have Xcode, CMake, and all relevant tools installed, so it was as simple as:

1. Install the latest version of Conan globally
   ```bash
   python -m pip install -U conan
   ```
1. Clone Audacity source code from GitHub

   ```bash
   git clone https://github.com/audacity/audacity/
   ```

1. Create a build directory and get into it
   ```
   cd audacity && \
   mkdir build && \
   cd build
   ```
1. Run CMake to generate the project - This part takes about 7 minutes as it downloads and builds all third-party packages from the [Conan Center Index](https://conan.io/center).
   ```bash
   cmake -GXcode ../
   ```
1. Open the generated project in Xcode
   ```bash
   open Audacity.xcodeproj
   ```
1. **Xcode**: Build all targets with **ALL_BUILD**; I've tried building only Audacity, but the `mod-script-pipe` is missing in the bare version of Audacity, so using **ALL_BUILD** is a must.
1. **Xcode**: Play the target **Audacity** that will build and start the application.

#### Let's Put It To The Test!

I'm super excited to run the tests against a locally built version of Audacity; I haven't changed anything yet in Audacity's code. First, I want to see the tests work as they're all new.

Bam! All tests passed **without noisy logs**. How could that be? I then realized that I'd built the latest branch of Audacity `master`, and I checked the Audacity version, and it's `3.5.0-alpha`.

Wait a minute. Does my application `audacity-scripting` work flawlessly with Audacity `3.5.0-alpha` on macOS? Let's try to build `3.4.2` locally to reproduce the issue. Following that, I'll check for differences with `git` between versions. Perhaps something big was changed in the `mod-script-pipe` module.

Sadly, the issue didn't reproduce, but this part is vague as I've built version `3.4.2-alpha` and had `3.4.2` installed from the [Audacity Downloads Page](https://www.audacityteam.org/download/).

#### Summary

I've decided to stop investigating the "macOS noisy logs" as I know that they will disappear in the next version of Audacity. I'll add to the docs that it's a known issue on `3.4.2` and should be resolved once `3.5.0` is officially out.
