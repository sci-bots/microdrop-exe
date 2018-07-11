REM chore(plugins): enable all plugins by default
%~dp0\microdrop-config edit --append plugins.enabled droplet_planning_plugin
%~dp0\microdrop-config edit --append plugins.enabled dmf_device_ui_plugin
%~dp0\microdrop-config edit --append plugins.enabled dropbot_plugin
%~dp0\microdrop-config edit --append plugins.enabled user_prompt_plugin
%~dp0\microdrop-config edit --append plugins.enabled step_label_plugin
REM perf(logging): set log level to `warning` to reduce logging overhead
%~dp0\microdrop-config edit --set microdrop\.app.log_level warning
