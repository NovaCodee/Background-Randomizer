const pix = document.getElementById('pix'); // checkbox for pixilate setting
const unsplash = document.getElementById('unsplash'); // checkbox for unsplash setting
const updateBg = document.getElementById("update_bg"); // button to update background
const updateSettings = document.getElementById("update_settings"); // button to update settings
const exit_btn = document.getElementById("exit_btn") // Button for Exiting GUI
const tags = document.getElementById("tags"); // input field for tags
const api = document.getElementById("api_id"); // input field for API key
const timer = document.getElementById("timer"); // input field for timer
const pixilation = document.getElementById("pixilation_input") // input field for Pixilation
const autostart = document.getElementById("autostart") // input field for Autostart
const autostart_gui = document.getElementById("autostart_gui") // input field for Autostart Gui
const autostart_gui_label = document.getElementById("autostart_gui_label") // label for Autostart Gui

// object to store config values to be updated
var configValues = {};

// Loads Config file at JS load
window.pywebview.api.load_config().then(initialConfig);

// add click event listener to update background button
updateBg.addEventListener("click", () => {  
    // call Python function to update background
    window.pywebview.api.call_bg_set();
});

// add click event listener to update settings button
updateSettings.addEventListener("click", () => {  
    // call function to update config values
    updateConfig();
});

// add clicl event listener to exit button
exit_btn.addEventListener("click", () => {  
  // call Python function to exit gui
  window.pywebview.api.toggle_gui_api();
});

// add change event listener to pixilate checkbox
pix.addEventListener('change', (event) => {
    // update configValues object with new value of pixilate setting
    configValues['PIXILATE'] = event.currentTarget.checked;
});

// add change event listener to unsplash checkbox
unsplash.addEventListener('change', (event) => {
    // update configValues object with new value of unsplash setting
    configValues['UNSPLASH'] = event.currentTarget.checked;
});

// add change event listener to autostart checkbox
autostart.addEventListener('change', (event) => {
  // update configValues object with new value of unsplash setting
  var value = event.currentTarget.checked;
  configValues['AUTOSTART'] = value;

  if (value == true){
    autostart_gui.classList.remove('hidden');
    autostart_gui_label.classList.remove('hidden');
  }else{
    configValues['AUTOSTART_GUI'] = false;
    autostart_gui.checked = false;
    autostart_gui.classList.add('hidden');
    autostart_gui_label.classList.add('hidden');
  }
});

// add change event listener to Gui Autostart checkbox
autostart_gui.addEventListener('change', (event) => {
  // update configValues object with new value of unsplash setting
  configValues['AUTOSTART_GUI'] = event.currentTarget.checked;
});

// add input event listener to tags input field
tags.addEventListener('input', (event) => {
  // update configValues object with new value of tags
  configValues['TAGS'] = event.target.value;
});

// add input event listener to api input field
api.addEventListener('input', (event) => {
  // update configValues object with new value of API key
  configValues['CLIENT_ID'] = event.target.value;
});

  // add input event listener to timner input field
timer.addEventListener('input', (event) => {
    // update configValues object with new value of API key
    configValues['SLIDESHOW_INTERVAL'] = event.target.value;
});
// add input event listener to Pixiliation Amount input field
pixilation.addEventListener('input', (event) => {
  // update configValues object with new value of API key
  configValues['PIXILATION_AMOUNT'] = event.target.value;
});

// callback function to update UI with initial config values
function initialConfig(output) {
  configValues = output
  // update checkbox values
  unsplash.checked = output['UNSPLASH'];
  pix.checked = output['PIXILATE'];
  autostart.checked = output['AUTOSTART']
  autostart_gui.checked = output['AUTOSTART_GUI']
  
  // update input field values
  api.value = output['CLIENT_ID'];
  tags.value = output['TAGS'];
  timer.value = output['SLIDESHOW_INTERVAL']
  pixilation.value = output['PIXILATION_AMOUNT']

  if (output['AUTOSTART'] == false){
    autostart_gui.classList.add('hidden');
    autostart_gui_label.classList.add('hidden');
  }
}

// function to update config values
function updateConfig() {
  // iterate over configValues object and call Python function to update each value
  window.pywebview.api.update_settings(configValues);
}
