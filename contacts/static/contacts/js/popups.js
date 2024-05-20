(function ($) {
  $(document).on('click', '.open-contact-popup', function () {

  }).on('submit', '#ajax-contact-form', function (event) {
    event.preventDefault();

      $.preloader();


      sendContactForm($(this), function () {
        $.popup().hide();
        // });
        return false;
      })



  }).on('submit', '#ajax-popup-contact-form', function () {
    // $.popup.showPreloader();
    // sendContactForm($(this), function () {
    //   $.popup.hidePreloader();
    // });
    // return false;
  });


  //
  function sendContactForm($form, callback) {
      if ($form.hasClass('sending')) {
        return false;
      }
      var data = new FormData($form.get(0));
      console.log(data)
      data.append('referer', location.href);

      return $.ajax({
        url: $form.prop('action'),
        type: 'POST',
        data: data,
        dataType: 'json',
        processData: false,
        contentType: false,
        beforeSend: function () {
          $form.addClass('sending');
          $form.find('.invalid').removeClass('invalid');
        },
        success: function (response) {

          if ($.isFunction(callback)) {
            callback();
          }

          if (response.url) {
            window.location.replace(response.url);
          }


          if (!response.success) {
            response.errors.forEach(function (record) {
              var $field = $form.find('.' + record.fullname);
              if ($field.length) {
                $field.addClass(record.class);
                $field.attr('data-after', record.errors[0]);
                $field.find('input').one('focus', function () {
                  $(this).parent().removeClass('invalid').removeAttr('data-after');
                })
              }
              if ((record.fullname.indexOf('recaptcha') + 1) && $form.find('div.g-recaptcha').length) {
                $form.removeClass('sending');
                window.grecaptcha.reset($form.find('div.g-recaptcha').attr('id'));
              }
            });
          }

        },
        error: function (response) {
          $.popup().hide();
          if (response && response.responseJSON && response.responseJSON.errors) {
            var errors = response.responseJSON.errors;

            errors.forEach(function (record) {
              var $field = $form.find('.' + record.fullname);
              if ($field.length) {
                $field.addClass(record.class);
                $field.attr('data-after', record.errors[0]);
              }
              if ((record.fullname.indexOf('recaptcha') + 1) && $form.find('div.g-recaptcha').length) {
                $form.removeClass('sending');
                window.grecaptcha.reset($form.find('div.g-recaptcha').attr('id'));
              }
            });
          }
        },
        complete: function () {


          $form.removeClass('sending');
          if (!$form.hasClass('no-preloader')) {
            $.popup().hide();
          }
          if ($form.find('div.g-recaptcha').length) {
            window.grecaptcha.reset($form.find('div.g-recaptcha').attr('id'));
          }
        }
      });

  }

})(jQuery);
