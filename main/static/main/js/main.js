$(document).ready(function() {
    function fade($ele) {
        $ele
            .fadeIn(1000)
            .delay(3000)
            .fadeOut(1000, function () {
                var $next = $(this).next(".quote");
                fade($next.length > 0 ? $next : $(this).parent().children().first());
            });
    }

    fade($(".quoteLoop > .quote").first());

    /* Navigation */
    $(window).scroll(function () {
        if ($(window).scrollTop() > 300) {
            $(".main_nav").addClass("sticky");
        } else {
            $(".main_nav").removeClass("sticky");
        }
    });

    // Mobile Navigation
    $(".mobile-toggle").click(function () {
        if ($(".main_nav").hasClass("open-nav")) {
            $(".main_nav").removeClass("open-nav");
        } else {
            $(".main_nav").addClass("open-nav");
        }
    });

    $(".main_nav li a").click(function () {
        if ($(".main_nav").hasClass("open-nav")) {
            $(".navigation").removeClass("open-nav");
            $(".main_nav").removeClass("open-nav");
        }
    });

    /* Smooth Scrolling */
    $(".smoothscroll").on("click", function (e) {
        e.preventDefault();

        var target = this.hash,
            $target = $(target);

        $("html, body")
            .stop()
            .animate(
                {
                    scrollTop: $target.offset().top
                },
                800,
                "swing",
                function () {
                    window.location.hash = target;
                }
            );
    });

    gsap.from(".heading", {opacity: 0, y: 20, duration: 0.8, delay: 0.2});

    // Выбор области загрузки
    const uploadArea = document.querySelector('#uploadArea');

    // Выбор области сброса
    const dropZoon = document.querySelector('#dropZoon');

    // Текст загрузки
    const loadingText = document.querySelector('#loadingText');

    // Выбор файла
    const fileInput = document.querySelector('#fileInput');

    // Предварительный просмотр изображения
    const previewImage = document.querySelector('#previewImage');

    // Область сведений о файле
    const fileDetails = document.querySelector('#fileDetails');

    // Загруженный файл
    const uploadedFile = document.querySelector('#uploadedFile');

    // Информация о загруженном файле
    const uploadedFileInfo = document.querySelector('#uploadedFileInfo');

    // Имя загруженного файла
    const uploadedFileName = document.querySelector('.uploaded-file__name');

    // Иконка загруженного файла
    const uploadedFileIconText = document.querySelector('.uploaded-file__icon-text');

    // Счетчик загруженного файла
    const uploadedFileCounter = document.querySelector('.uploaded-file__counter');

    // Данные подсказки
    const toolTipData = document.querySelector('.upload-area__tooltip-data');

    // Типы изображений
    const imagesTypes = [
        "jpeg",
        "png",
        "svg"
    ];

    // Добавление типов изображений в подсказку
    toolTipData.innerHTML = [...imagesTypes].join(', .');

    // Обработчики событий для области загрузки
    dropZoon.addEventListener('dragover', function (event) {
        event.preventDefault();
        dropZoon.classList.add('drop-zoon--over');
    });

    dropZoon.addEventListener('dragleave', function (event) {
        dropZoon.classList.remove('drop-zoon--over');
    });

    dropZoon.addEventListener('change', function (event) {
        event.preventDefault();
        dropZoon.classList.remove('drop-zoon--over');
        const file = event.target.files[0];
        uploadFile(file);
    });

    // Функция загрузки файла
    function uploadFile(file) {
        const fileReader = new FileReader();
        const fileType = file.type;
        const fileSize = file.size;

        if (fileValidate(fileType, fileSize)) {
            dropZoon.classList.add('drop-zoon--Uploaded');
            loadingText.style.display = "block";
            uploadedFile.classList.remove('uploaded-file--open');
            uploadedFileInfo.classList.remove('uploaded-file__info--active');

            fileReader.addEventListener('load', function () {
                setTimeout(function () {
                    uploadArea.classList.add('upload-area--open');
                    previewImage.style.display = 'block';
                    fileDetails.classList.add('file-details--open');
                    uploadedFile.classList.add('uploaded-file--open');
                    uploadedFileInfo.classList.add('uploaded-file__info--active');

                    setTimeout(function () {
                        document.getElementById('uploadButton').classList.add('show');
                    }, 800);

                }, 500);

                document.getElementById('uploadButton').onclick = pushButton;
                function pushButton() {
                    window.location.href = '#model'
                }

                previewImage.setAttribute('src', fileReader.result);
                uploadedFileName.innerHTML = file.name;
                progressMove();
            });

            fileReader.readAsDataURL(file);

            setTimeout(function () {
                $('#team-anchor').fadeOut('slow');
            }, 300);
        }
    }

//    // Без перезагрузок, ура!
//    document.querySelector('form').addEventListener('submit', function(e) {
//      e.preventDefault();
//    });

    // Функция увеличения счетчика прогресса
    function progressMove() {
        let counter = 0;

        setTimeout(() => {
            let counterIncrease = setInterval(() => {
                if (counter === 100) {
                    clearInterval(counterIncrease);
                } else {
                    counter = counter + 10;
                    uploadedFileCounter.innerHTML = `${counter}%`
                }
            }, 100);
        }, 600);
    }


    // Функция валидации файла
    function fileValidate(fileType, fileSize) {
        let isImage = imagesTypes.filter((type) => fileType.indexOf(`image/${type}`) !== -1);

        if (isImage[0] === 'jpeg') {
            uploadedFileIconText.innerHTML = 'jpg';
        } else {
            uploadedFileIconText.innerHTML = isImage[0];
        }

        if (isImage.length !== 0) {
            if (fileSize <= 2000000) {
                return true;
            } else {
                alert('Пожалуйста, загрузите файл размером не более 2 Мегабайт');
                return false;
            }
        } else {
            alert('Пожалуйста, убедитесь, что загружаемый файл является изображением');
            return false;
        }
    }

})

