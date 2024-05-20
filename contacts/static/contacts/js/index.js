(function ($) {

  var contactPhone = $('#id_phone');
  if (contactPhone.length) {
    contactPhone.mask('(000) 000-0000');
  }

  if (document.querySelectorAll('.form').length != 0) {
    let labels = document.querySelectorAll(".form__label");
    let inputs = document.querySelectorAll(".form__input");
    for (let i = 0; i < inputs.length; i++) {
      let input = inputs[i];
      let label = labels[i];
      if (label.classList.contains("form__label-column")) {
        if (input.value !== '') {
          label.classList.add("form__label-column--focus");
        }
        input.addEventListener('focus', function () {
          label.classList.add("form__label-column--focus");
        })
      } else {
        if (input.value !== '') {
          label.classList.add("form__label--focus");
        }
        input.addEventListener('focus', function () {
          label.classList.add("form__label--focus");
        })
      }
      input.addEventListener('blur', function () {
        if (input.value === '') {
          label.classList.remove("form__label--focus");
          label.classList.remove("form__label-column--focus");
        }
      });
    }

    $('input, textarea').on('focus', function () {
      $(this).parent().addClass('focus');
    });
    $('input, textarea').on('blur', function () {
      $(this).parent().removeClass('focus');
    });
  }


  if ($('.form-adviser').length) {

    $('#id_marital_status_0-2').change(function () {
      if (this.checked == true) {
        const array = document.querySelectorAll('.form__status');
        for (var i = 0; i < array.length; ++i) {
          array[i].classList.remove('form__large-row--hidden');
        }
      }
    });

    $('#id_marital_status_0-1').change(function () {
      if (this.checked == true) {
        const array = document.querySelectorAll('.form__status');
        for (var i = 0; i < array.length; ++i) {
          array[i].classList.add('form__large-row--hidden');
        }
      }
    });

    $('#id_read_fee_structure_0-2').change(function () {
      if (this.checked == true) {
        window.open("/about/fee-structure/", '_blank')
      }
    });
    let popUp = document.querySelector(".modal--js");
    let popUpClose = document.querySelector(".modal__close--js");
    let body = document.body;
    let header = document.querySelector(".header");


    popUpClose.addEventListener("click", function () {
      popUp.classList.remove("modal--open");
      body.classList.remove("overflow");
      header.classList.remove("header--hidden");
      $("body").removeClass("compensate-for-scrollbar");
    });

    window.addEventListener("keydown", function (event) {
      if (
        popUp.classList.contains("modal--open") &&
        event.code === "Escape"
      ) {
        popUp.classList.remove("modal--open");
        body.classList.remove("overflow");
        header.classList.remove("header--hidden");
        $("body").removeClass("compensate-for-scrollbar");
      }
    });


    $.fn.datepicker.language['en'] = {
      days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      daysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      daysMin: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
      months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
      today: 'Today',
      clear: 'Clear',
      dateFormat: 'mm/dd/yyyy',
      timeFormat: 'hh:ii',
      firstDay: 1
    };

    var startDateDatepickerHere = function () {
      var date = new Date();
      return new Date(date.setDate(date.getDate() + 2));
    };

    var disabledDays = [0, 6];

    $('.datepicker-here').datepicker({
      language: 'en',
      minDate: startDateDatepickerHere(),
      // dateFormat: 'yyyy-dd-mm',
      position: "bottom center",
      autoClose: true,
      firstDay: 0,
      onRenderCell: function (date, cellType) {
        if (cellType == 'day') {
          var day = date.getDay(),
            isDisabled = disabledDays.indexOf(day) != -1;

          return {
            disabled: isDisabled
          }
        }
      }
    });
    $('.form__input_date').mask('00/00/0000');
    $('.form__input_date--birth').mask('00/00/0000');
    $('.form__input_phone').mask('(000) 000-0000');

    var formData = '';
    $('.form-adviser').validate({
      rules: {
        "name": {
          required: true
        },
        "email": {
          required: true,
          email: true
        },
        "phone": {
          required: true,
          minlength: 14
        },

      },
      messages: {
        "name": "Please enter your name",
        "email": {
          required: "Please enter your e-mail so we can contact you",
          email: "Your email address must be in the format of name@domain.com"
        },
        "phone": {
          required: "Please enter your phone so we can contact you"
        },
        "date_convenient": {
          required: "This field is required"
        },
      },
      errorElement: 'span',
      focusCleanup: true,
      highlight: function (element, errorClass) {
        $(element).parent().addClass(errorClass);
      },
      unhighlight: function (element, errorClass) {
        $(element).parent().removeClass(errorClass);
      },
      submitHandler: function (form) {
        formData = '';
        formData = new FormData(document.querySelector('.form-adviser'));
        $("head").append(
          '<style id="noscroll" type="text/css">.compensate-for-scrollbar{margin-right:' +
          (window.innerWidth - document.documentElement.clientWidth) +
          "px;}</style>"
        );
        $("body").addClass("compensate-for-scrollbar");
        popUp.classList.add("modal--open");
        body.classList.add("overflow");
        header.classList.add("header--hidden");
        document.querySelector(':root').style
          .setProperty('--vh', window.innerHeight / 100 + 'px');
      }
    })


    $.validator.addMethod("anyDate",
      function (value, element) {
        return value.match(/^(0?[1-9]|1[0-2])[/., -](0?[1-9]|[12][0-9]|3[0-1])[/., -](19|20)?\d{4}$/);
      },
      "Please enter a valid date"
    );

    $.validator.methods.email = function (value, element) {
      return this.optional(element) || /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))+@[a-z]+\.[a-z]+/.test(value);
    }

    var isVerified = false;
    var formValidate_2 = null;

    $('.form-adviser_two').on('submit', function (event) {
      event.preventDefault();

        if (!$('#id_marital_status_0-2').is(':checked')) {
          if (formValidate_2) {
            formValidate_2.destroy();
            formValidate_2 = null;
          }
          $.validator.setDefaults({
            ignore: '#id_spouse_date_birth'
          });
          $.validator.setDefaults({
            ignore: '#id_spouse_name'
          });
          $.validator.setDefaults({
            ignore: '#id_spouse_retirement'
          });
          $.validator.setDefaults({
            ignore: '#id_spouse_occupation'
          });


        } else {
          if (formValidate_2) {
            formValidate_2.destroy();
            formValidate_2 = null;
          }
          $.validator.setDefaults({
            ignore: ':hidden'
          });
        }


    });


    $('.form-adviser_two').validate({
      rules: {

        "spouse_name": {
          required: true
        },
        "social_media": {
          required: true
        },
        "professional_guidance": {
          required: true
        },
        "agree": {
          required: true
        },
        "spouse_retirement": {
          required: true
        },
        "date_of_birth": {
          required: true,
          anyDate: true
        },
        "spouse_date_birth": {
          required: true,
          anyDate: true
        },
        "occupation": {
          required: true
        },
        "spouse_occupation": {
          required: true
        },
        "household_income": {
          required: true
        },
        "investeble_assets": {
          required: true
        },
        "number_of_children": {
          required: true
        },

        "how_did_you_hear_about_us": {
          required: true
        },
        "additional_information": {
          required: false
        },

      },
      messages: {
        "spouse_name": {
          required: "This field is required"
        },
        "social_media": {
          required: "This field is required"
        },
        "agree": {
          required: "This field is required"
        },
        "spouse_retirement": {
          required: "This field is required"
        },
        "date_of_birth": {
          required: "This field is required",
          anyDate: 'Please enter a valid date'
        },
        "spouse_date_birth": {
          required: "This field is required",
          anyDate: 'Please enter a valid date'
        },
        "occupation": {
          required: "This field is required"
        },
        "spouse_occupation": {
          required: "This field is required"
        },
        "household_income": {
          required: "This field is required"
        },
        "investeble_assets": {
          required: "This field is required"
        },
        "number_of_children": {
          required: "This field is required"
        },
        "how_did_you_hear_about_us": {
          required: "This field is required"
        },
        "professional_guidance": {
          required: "This field is required"
        },
      },
      errorElement: 'span',
      focusCleanup: true,
      highlight: function (element, errorClass) {
        $(element).parent().addClass(errorClass);
      },
      unhighlight: function (element, errorClass) {
        $(element).parent().removeClass(errorClass);
      },
      submitHandler: function (form) {
        var $form = $(form);

        var poData = $form.serializeArray();

        var newData = formData;

        for (var i = 0; i < poData.length; i++) {
          newData.append(poData[i].name, poData[i].value);
        }
        var data = newData;
        data.append('referer', location.href);

          $.ajax({
            url: $form.attr('action'),
            type: 'POST',
            data: data,
            dataType: 'json',
            processData: false,
            contentType: false,
            beforeSend: function () {
              $.preloader();
              $form.addClass('sending');
              $form.find('.invalid').removeClass('invalid');
            },
            success: function (response) {

              if (response.url) {
                window.location.replace(response.url);
              }
            },
            complete: function () {
              $form.removeClass('sending');
            }
          });

      }
    })

  }

})(jQuery);

