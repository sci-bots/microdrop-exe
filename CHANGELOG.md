# 2.21.1

 - MicroDrop 2.21.1 including the following plugins:
   - microdrop.dmf-device-ui-plugin 2.6
   - microdrop.dropbot-plugin  2.23
   - microdrop.droplet-planning-plugin 2.3.1
   - microdrop.step-label-plugin 2.2.2
   - microdrop.user-prompt-plugin 2.3.1

See `releases/environment-2.21.1.yaml`.

## Upstream changes

 - [x] Build fixed `teensy-minimal-rpc` with support for `library.zip` (`dropbot::teensy-minimal-rpc(-dev)==0.10`)
 - [x] Build fixed `jupyter-helpers` package, with updated regular expression (`dropbot::jupyter-helpers==0.11`)
 - [x] Build fixed `pygtkhelpers` package, with support for `library.zip` (`wheeler-microfluidics::wheeler.pygtkhelpers==0.21-0`)
   - [x] Build `debounce` package as `python: noarch` (`wheeler-microfluidics::debounce==0.2`)
 - [x] Build fixed `platformio-core` with support for `library.zip` (`dropbot::platformio==3.5.2b2.post20-g42c1c804_0`):
   * Patch `platformio.util` to look for source files in
     `<prefix>/platformio`:
     ```python
     ...
     def get_source_dir():
         if sys.frozen:
             return os.path.join(sys.prefix, 'platformio')
     ...
     ```
 - [x] Build fixed `microdrop` package, with support for `library.zip` (`wheeler-microfluidics::microdrop==2.21.1`)
   - [x] Build `path_helpers` package, with `resource_copytree` (`wheeler-microfluidics::path_helpers==0.8`)
