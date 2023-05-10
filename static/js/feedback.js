$(function () {
  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-feedback .modal-content").html("");
        $("#modal-feedback").modal("show");
      },
      success: function (data) {
        $("#modal-feedback .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#modal-feedback .modal-content").html('<div class="feedback_send">Thanks for your feedback</div>');
          setTimeout(() => {
          $("#modal-feedback").modal("hide");
          }, 2000)
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  $(".js-feedback").click(loadForm);
  $("#modal-feedback").on("submit", ".js-feedback-form", saveForm);

});
