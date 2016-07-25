$(function(){
	function passwordMatch(pw, pwConf, submit) {
		var password;
		pw.on('focusout', function(){
			password = $(this).val();
			return password;
		})
		pwConf.on('keyup', function(){
			var passwordConf = $(this).val();
			if (passwordConf !== password) {
				$(this).css({'color':'red'});
				submit.prop("disabled",true);
			}else {
				$(this).css({'color': 'black'});
				submit.removeAttr("disabled");
			}
		})
	}
	passwordMatch($('#regPassword'), $('#regPasswordConf'), $('#regSubmit'));
	passwordMatch($('#editPassword'), $('#editPasswordConf'), $('#updateSubmit'));
	
	$('input').on('focusin', function(){
		$(this).siblings('.errMsg').hide();
	})
	$('#showInfo').on('click', function(){
		var names = ['first_name','last_name','email'];
		for(var i=0; i<names.length; i++) {
			$('.editForm .form-group input[name="'+names[i]+'"]').val($('.editForm .form-group input[name="'+names[i]+'_hd"]').val());
		}
	})
	$('#n_showInfo').on('click', function(){
		var names = ['first_name','last_name','email', 'description'];
		for(var i=0; i<names.length; i++) {
			$('.n_editForm .form-group input[name="'+names[i]+'"]').val($('.n_editForm .form-group input[name="'+names[i]+'_hd"]').val());
		}
	})
	$('.nedit').on('keyup', function(){
		inputIds = ['n_editfName', 'n_editlName', 'n_editEmail', 'n_editDescription', 'n_editPassword', 'n_editPasswordConf'];
		for (var i=0; i<inputIds.length; i++){
			if ($('#'+inputIds[i]).val() === '') {
				$('#n_updateSubmit').prop('disabled', true);
			}else {
				$('#n_updateSubmit').removeAttr('disabled');
			}
		}
	})
	passwordMatch($('#n_editPassword'), $('#n_editPasswordConf'), $('#n_updateSubmit'));
})