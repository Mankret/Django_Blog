// Contact Us
$(function () {

    var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#contact_us .modal-content").html("");
        $("#contact_us").modal("show");


      },
      success: function (data) {
        $("#contact_us .modal-content").html(data.html_form);

      }
    });
  };

  var sendForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
            $("#contact_us").modal("hide");


        }
        else {
               $("#contact_us .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };




  // Send message
  $(".js-contact-us").click(loadForm);
  $("#contact_us").on("submit", ".js-send-form", sendForm);


});