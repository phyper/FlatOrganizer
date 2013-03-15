//####################
// index.html
//####################

// Validate the form content - editFlatForm
$(document).ready(function()
{
    // Validation
    $("#editFlatForm").validate({
        rules:{
            name: "required",
            description:{required:true, maxlength: 200}
        },

        errorClass: "help-inline",
        errorElement: "span",
        highlight:function(element, errorClass, validClass)
        {
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass)
        {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });
});

// Validate the form content - createFlatForm
$(document).ready(function()
{
    // Validation
    $("#createFlatForm").validate({
        rules:{
            name: "required",
            description:{required:true, maxlength: 200}
        },

        errorClass: "help-inline",
        errorElement: "span",
        highlight:function(element, errorClass, validClass)
        {
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass)
        {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });
});

// Hide and show invite box
$(document).ready(function(){
    $(function() {
        $(document).on('click', '.inviteBox', function(e) {
            var $this = $(this);
            if ($this.next().is(":hidden")) {
                $this.next().slideDown("slow");
            } else {
                $this.next().slideUp("slow");
            }
        });
    });
});


// Script to get the id of Flat_member of a row

function getFlatMemberId(para){
    document.getElementById('leaveFlat').value = para;
}
$(document).ready(function(){
    $(function() {
        $(document).on('click', '.removeFlatButton', function(e) {
            var para = this.dataset['para'];
            getFlatMemberId(para);
        });
    });
});


// Script to get the id of Flat of a row

function getFlatId(para){
    document.getElementById('editFlat').value = para;
}
$(document).ready(function(){
    $(function() {
        $(document).on('click', '.editFlatInfoButton', function(e) {
            var para = this.dataset['para'];
            getFlatId(para);
        });
    });
});

// Script to get the id of Flat of a row for edit flat

$(document).ready(function(){
    $(function() {
        $(document).on('click', '.editFlatInfoButton', function(e) {
            var name = this.dataset['para1'];
            var desc = this.dataset['para2'];
            $('#editFlatName').val(name);
            $('#editFlatDescription').val(desc);
        });
    });
});



//####################
// flat.html
//####################

// Validate the form content - create new item

$(document).ready(function()
{
    // Validation
    $("#createItemForm").validate({
        rules:{
            name: {required: true, maxlength: 50},
            description:{required:true, maxlength: 100},
            credits: {required:true, whole: true},
            category: {required: true}
        },

        errorClass: "help-inline",
        errorElement: "span",
        highlight:function(element, errorClass, validClass)
        {
            $(element).parents('.control-group').addClass('error');
        },
        unhighlight: function(element, errorClass, validClass)
        {
            $(element).parents('.control-group').removeClass('error');
            $(element).parents('.control-group').addClass('success');
        }
    });

    $('.dropdown-toggle').dropdown();

});

$(function() {
    $(document).on('click', '#deleteTaskIcon', function(e) {
        var para = this.dataset['para'];
        $('#task_id_modal').val(para);
    });
});
$(function() {
    $(document).on('click', '#deleteTaskIcon2', function(e) {
        var para = this.dataset['para'];
        $('#task_id_modal').val(para);
    });
});

//####################
// register.html
//
// Modified from: http://www.9lessons.info/2012/04/bootstrap-registration-form-tutorial.html
//###################

    $(document).ready(function()
    {
    // Popover
    $('#registerHere input').hover(
      function(){
        $(this).popover('show')
      },
      function(){
        $(this).popover('hide')
       }
    );

    // Validation
    $("#registerHere").validate({
      rules:{
      first_name: "required",
      last_name: "required",
      username:"required",
      email:{required:true,email: true},
      password1:{required:true,minlength: 6},
      password2:{required:true,equalTo: "#password1"}
    },

    messages:{
      first_name: "Enter your first name",
      last_name: "Enter your last name",
      username:"Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
      email:{
        required:"Enter your email address",
        email:"Enter valid email address"},
      password1:{
        required:"Enter your password",
        minlength:"Password must be minimum 6 characters"},
      password2:{
        required:"Enter confirm password",
        equalTo:"Password and Confirm Password must match"}
    },

    errorClass: "help-inline",
    errorElement: "span",
    highlight:function(element, errorClass, validClass)
    {
      $(element).parents('.control-group').addClass('error');
    },
    unhighlight: function(element, errorClass, validClass)
    {
      $(element).parents('.control-group').removeClass('error');
      $(element).parents('.control-group').addClass('success');
    }
    });
});
