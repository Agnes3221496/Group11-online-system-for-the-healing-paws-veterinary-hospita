	$(document).ready(function () {
    console.log("Adding event handlers");
    $("#username").on("change", check_username)
    $("#email").on("change", check_email);
    console.log("function registered");
    });


function check_username() {
    // get the source element
    console.log("check_username called");
    var chosen_user = $(this).find("input");
    console.log("User chose: " + chosen_user.val());

    $("#checkuser").removeClass();
    $("#checkuser").html('<img src="static/style/loading.gif")>');

    // ajax code
    $.post('/checkuser', {
        'username': chosen_user.val() //field value being sent to the server
    }).done(function (response) {
        var server_response = response['text']
        var server_code = response['returnvalue']
        console.log(server_code);
        if (server_code == 0) { // success: Username does not exist in the database
            $("#password").focus();
            $("#checkuser").html('<span>' + server_response + '</span>');
            $("#checkuser").addClass("success");
        } else { // failure: Username already exists in the database
            chosen_user.val("");
            chosen_user.focus();
            $("#checkuser").html('<span>' + server_response + '</span>');
            $("#checkuser").addClass("failure");
        }
    }).fail(function () {
        $("#checkuser").html('<span>Error contacting server</span>');
        $("#checkuser").addClass("failure");
    });
    // end of ajax code

    console.log("finished check_username");

}

function check_email() {
    console.log('check_email called');
    let chosen_email = $(this).find("input");
    console.log('user email:' + chosen_email.val());

    $('#checkemail').removeClass();
    $('#checkemail').html('<img src="../images/loading.gif">');

    $.post('/checkemail', {
        'email': chosen_email.val()
    })
    .done(function (response) {
        let server_response = response['text'];
        let server_code = response['returnvalue'];
        console.log(server_code);

        console.log(server_code);

        if (server_code==2) {
            $("#password").focus();
            $("#checkemail").html('<span>' + server_response + '</span>');
            $("#checkemail").addClass('success');
            chosen_email.val(chosen_email.val());
            console.log('success')
        } else {
            chosen_email.val("");
            chosen_email.focus();
            $("#checkemail").html('<span>' + server_response + '</span>');
            $("#checkemail").addClass('failure');
            console.log('fail')
        }
    }).fail(function() {
		$("#checkemail").html('<span>Error contacting server</span>');
		$("#checkemail").addClass("failure");

	});
	console.log("finished check_email");}

