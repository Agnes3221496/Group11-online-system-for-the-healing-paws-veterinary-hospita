$(document).ready(function () {
    $('#i18n').on('change', change_lan);
})

function change_lan(){
    defaultLanguage = $('#i18n').val();
    console.log('change i18n')
    console.log(defaultLanguage)
    $.ajax({
        type: 'GET',
        url: '/chooseLan',
        data: {
            language: defaultLanguage.val()
        },
        success: function (data) {
            alert(data)
            // location.reload();
        },
        error: function (data) {
            alert('fail')
        }
	});
}
