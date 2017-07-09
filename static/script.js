(function () {
    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            var submitButton = event.target.querySelector('input[type=submit]');
            submitButton.disabled = true;
            var data = new FormData(form);
            var xhr = new XMLHttpRequest();
            xhr.addEventListener('load', function () {
                submitButton.disabled = false;

                var docElement = event.target.parentElement.parentElement;
                if (data.get('interesting') === 'yes') {
                    docElement.classList.add('interesting');
                    docElement.classList.remove('boring');
                } else {
                    docElement.classList.remove('interesting');
                    docElement.classList.add('boring');
                }
            });
            xhr.addEventListener('error', function() {
                alert('Request failed!');
                submitButton.disabled = false;
            });
            xhr.open("POST", form.action);
            xhr.send(data);
        });
    });
})();
