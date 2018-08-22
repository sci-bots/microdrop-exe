REM chore(plugins): enable all plugins by default
%~dp0\microdrop-config edit --append plugins.enabled droplet_planning_plugin
%~dp0\microdrop-config edit --append plugins.enabled dmf_device_ui_plugin
%~dp0\microdrop-config edit --append plugins.enabled dropbot_plugin
%~dp0\microdrop-config edit --append plugins.enabled user_prompt_plugin
%~dp0\microdrop-config edit --append plugins.enabled step_label_plugin
REM perf(logging): set log level to `info` to reduce logging overhead
%~dp0\microdrop-config edit --set microdrop\.app.log_level info
REM chore(device-ui): hide connections layer by default
%~dp0\microdrop-config edit --set dmf_device_ui_plugin.surface_alphas "{""background"":1.0,""shapes"":1.0,""connections"":0.0,""routes"":1.0,""channel_labels"":1.0,""actuated_shapes"":1.0,""registration"":0.0}"
