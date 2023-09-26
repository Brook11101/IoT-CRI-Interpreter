document.addEventListener("DOMContentLoaded", function() {
    // 在页面加载完成后执行 JavaScript
    // 创建 Monaco Editor 实例
    require.config({ paths: { 'vs': 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.23.0/min/vs' } });
    require(['vs/editor/editor.main'], function () {
        var editor = monaco.editor.create(document.getElementById('editor'), {
            value: 'console.log("Hello, TypeScript!");',
            language: 'typescript',
            automaticLayout: true
        });
    });
});