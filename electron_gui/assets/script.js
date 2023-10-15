window.editor = null;

document.addEventListener("DOMContentLoaded", function () {
    require.config({paths: {'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.23.0/min/vs'}});
    require(['vs/editor/editor.main'], function () {
        window.editor = monaco.editor.create(document.getElementById('editor'), {
            value: '// Write your filter code here;',
            language: 'typescript',
            automaticLayout: true,
            glyphMargin: false,
            minimap: {
                enabled: false
            }
        });
    });
});

window.getEditorContent = function() {
    return window.editor ? window.editor.getValue() : "null!";
}