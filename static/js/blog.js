document.addEventListener("DOMContentLoaded", function () {
    const copyBtn = document.getElementById("copyLinkBtn");
    const copyText = document.getElementById("copyLinkText");

    if (copyBtn) {
        copyBtn.addEventListener("click", function () {
            const url = copyBtn.getAttribute("data-url") || window.location.href;

            const fallbackCopy = function () {
                const textarea = document.createElement("textarea");
                textarea.value = url;
                textarea.style.position = "fixed";
                textarea.style.opacity = "0";
                document.body.appendChild(textarea);
                textarea.select();
                try {
                    document.execCommand("copy");
                } catch (e) {
                    console.error("Copy failed", e);
                }
                document.body.removeChild(textarea);
            };

            const showCopied = function () {
                const original = copyText.textContent;
                copyText.textContent = "Copied!";
                copyBtn.classList.add("btn-success");
                copyBtn.classList.remove("btn-outline-primary");
                setTimeout(function () {
                    copyText.textContent = original;
                    copyBtn.classList.remove("btn-success");
                    copyBtn.classList.add("btn-outline-primary");
                }, 2000);
            };

            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(url).then(showCopied).catch(function () {
                    fallbackCopy();
                    showCopied();
                });
            } else {
                fallbackCopy();
                showCopied();
            }
        });
    }
});
