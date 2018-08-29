REM chore(plugins): enable all plugins by default
%~dp0\microdrop-config edit --append plugins.enabled droplet_planning_plugin
%~dp0\microdrop-config edit --append plugins.enabled dmf_device_ui_plugin
%~dp0\microdrop-config edit --append plugins.enabled dropbot_plugin
%~dp0\microdrop-config edit --append plugins.enabled user_prompt_plugin
%~dp0\microdrop-config edit --append plugins.enabled step_label_plugin
REM perf(logging): set log level to `info` to reduce logging overhead
%~dp0\microdrop-config edit --set microdrop\.app.log_level info
REM chore(device-ui): hide connections layer by default
%~dp0\microdrop-config edit --set dmf_device_ui_plugin.surface_alphas "{""background"":1.0,""shapes"":1.0,""connections"":0.0,""routes"":1.0,""channel_labels"":1.0,""static_electrode_state_shapes"":0.7,""dynamic_electrode_state_shapes"":0.7,""registration"":0.0}"
REM chore(protocol-grid-controller): set default column positions
%~dp0\microdrop-config edit --set microdrop\.gui\.protocol_grid_controller.column_positions "{""Trail length"": 6, ""Message"": 7, ""Id"": 0, ""Duration (s)"": 2, ""Frequency (hz)"": 9, ""Video"": 10, ""Voltage (v)"": 3, ""Volume threshold"": 8, ""Repeat duration s"": 4, ""Route repeats"": 5, ""Schema"": 1}"
