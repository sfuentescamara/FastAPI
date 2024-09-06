ref: https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu

ffmpeg="~/sd_card/ffmpeg"

## Dependencies
sudo apt-get -y install \
  autoconf \
  automake \
  build-essential \
  cmake \
  git-core \
  libass-dev \
  libfreetype6-dev \
  libgnutls28-dev \
  libmp3lame-dev \
  libsdl2-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  meson \
  ninja-build \
  pkg-config \
  texinfo \
  wget \
  yasm \
  zlib1g-dev

## INSTALL h264
git -C x264 pull 2> /dev/null || git clone --depth 1 https://code.videolan.org/videolan/x264.git && \
cd x264 && \
PATH="$ffmpeg/bin:$PATH" PKG_CONFIG_PATH="$ffmpeg/ffmpeg_build/lib/pkgconfig" ./configure --prefix="$ffmpeg/ffmpeg_build" --bindir="$ffmpeg/bin" --enable-static --enable-pic && \
PATH="$ffmpeg/bin:$PATH" make && \
make install

## INSTALL h265
wget -O x265.tar.bz2 https://bitbucket.org/multicoreware/x265_git/get/master.tar.bz2 && \
tar xjvf x265.tar.bz2 && \
cd multicoreware*/build/linux && \
PATH="$ffmpeg/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$ffmpeg/ffmpeg_build" -DENABLE_SHARED=off ../../source && \
PATH="$ffmpeg/bin:$PATH" make && \
make install

## INSTALL libvpx
git -C libvpx pull 2> /dev/null || git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git && \
cd libvpx && \
PATH="$ffmpeg/bin:$PATH" ./configure --prefix="$ffmpeg/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm && \
PATH="$ffmpeg/bin:$PATH" make && \
make install

### (Needs dependencies)
## INSTALL libfdk-aac (AAC audio encoder) 
git -C fdk-aac pull 2> /dev/null || git clone --depth 1 https://github.com/mstorsjo/fdk-aac && \
cd fdk-aac && \
autoreconf -fiv && \
./configure --prefix="$ffmpeg/ffmpeg_build" --disable-shared && \
make && \
make install


## INSTALL libopus (Opus audio decoder and encoder)
### Fail
git -C opus pull 2> /dev/null || git clone --depth 1 https://github.com/xiph/opus.git && \
cd opus && \
./autogen.sh && \
./configure --prefix="$ffmpeg/ffmpeg_build" --disable-shared && \
make && \
make install

## INSTALL libaom (AV1 video encoder/decoder)
git -C aom pull 2> /dev/null || git clone --depth 1 https://aomedia.googlesource.com/aom && \
mkdir -p aom_build && \
cd aom_build && \
PATH="$ffmpeg/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$ffmpeg/ffmpeg_build" -DENABLE_TESTS=OFF -DENABLE_NASM=on ../aom && \
PATH="$ffmpeg/bin:$PATH" make && \
make install

## INSTALL libsvtav1 (AV1 video encoder/decod)
git -C SVT-AV1 pull 2> /dev/null || git clone https://gitlab.com/AOMediaCodec/SVT-AV1.git && \
mkdir -p SVT-AV1/build && \
cd SVT-AV1/build && \
PATH="$ffmpeg/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$ffmpeg/ffmpeg_build" -DCMAKE_BUILD_TYPE=Release -DBUILD_DEC=OFF -DBUILD_SHARED_LIBS=OFF .. && \
PATH="$ffmpeg/bin:$PATH" make && \
make install

## INSTALL libdav1d (AV1 decoder faster)
git -C dav1d pull 2> /dev/null || git clone --depth 1 https://code.videolan.org/videolan/dav1d.git && \
mkdir -p dav1d/build && \
cd dav1d/build && \
meson setup -Denable_tools=false -Denable_tests=false --default-library=static .. --prefix "$ffmpeg/ffmpeg_build" --libdir="$ffmpeg/ffmpeg_build/lib" && \
ninja && \
ninja install

## INSTALL libvmaf
wget https://github.com/Netflix/vmaf/archive/v3.0.0.tar.gz && \
tar xvf v3.0.0.tar.gz && \
mkdir -p vmaf-3.0.0/libvmaf/build &&\
cd vmaf-3.0.0/libvmaf/build && \
meson setup -Denable_tests=false -Denable_docs=false --buildtype=release --default-library=static .. --prefix "$ffmpeg/ffmpeg_build" --bindir="$ffmpeg/bin" --libdir="$ffmpeg/ffmpeg_build/lib" && \
ninja && \
ninja install



## INSTALL ffmpeg
wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 && \
tar xjvf ffmpeg-snapshot.tar.bz2 && \
cd ffmpeg && \
PATH="$ffmpeg/bin:$PATH" PKG_CONFIG_PATH="$ffmpeg/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$ffmpeg/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$ffmpeg/ffmpeg_build/include" \
  --extra-ldflags="-L$ffmpeg/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --ld="g++" \
  --bindir="$ffmpeg/bin" \
  --enable-gpl \
  --enable-openssl \
  --enable-libaom \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libsvtav1 \
  --enable-libdav1d \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree && \
PATH="$ffmpeg/bin:$PATH" make && \
make install && \
hash -r

