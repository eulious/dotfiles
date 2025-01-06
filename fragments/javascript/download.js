function textSave(name, text) {
  var blob = new Blob([text], { type: 'text/plain' });
  var link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = name + '.txt';
  link.click();
}
