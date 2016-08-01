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

	// Front-end validation
	var email_regex = /^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$/
	var keyArr = {'first_name':1, 'last_name':1, 'email':1, 'password':8, 'msgContent':1, 'cmtContent':1};
	var errMsg = {};
	var error = false;
	$('.validate').on('keyup', function(){
		var name = $(this).attr('name');
		var testInput = $(this).val();
		var thisLen = testInput.length;
		if (thisLen < keyArr[name]) {
			error = true;
			errMsg[name] = "<p class='errMsg'>"+name+ " must be more than "+ keyArr[name]+" characters.</p>";
		}else {
			error = false;
			delete errMsg[name];
		}
		if (name === 'email' && !email_regex.test(testInput)) {
			error = true;
			errMsg[name+'Invalid'] = "<p class='errMsg'>Invalid email.</p>"
		}
		var html = '';
		if(error) {
			$.each(errMsg, function(key, val){
				if(key.indexOf(name)>=0){
					html += val;
				}
			})
			$('input[name="'+name+'"]').addClass('errInput');
		}else {
			$('input[name="'+name+'"]').removeClass('errInput');
		}
		$('input[name="'+name+'"]').siblings('.showErr').html(html);
	})
	$('#loginPassword').on('keyup', function(){
		if ($(this).siblings('.showErr').is(':empty')){
			$(this).parent().siblings('button[type="submit"]').removeAttr('disabled');
		}
	})
	$('input').on('focusin', function(){
		$(this).siblings('.showErr').html('');
	})
	$('#post').on('keyup', function(){
		if ($(this).val()!==''){
			$(this).siblings('button').removeAttr('disabled');			
		}
	})
	$('.cmtBox').on('keyup', function(){
		if ($(this).val()!==''){
			$(this).siblings('input[type="submit"]').removeAttr('disabled');			
		}
	})

	// Live validation front+back end. Deprecated due to big server load
	// function validation(key, title){
	// 	var token = $(".lrForm").find('input[name=csrfmiddlewaretoken]').val();
	// 	var keyArr = {'first_name':2, 'last_name':2, 'email':1, 'password':8};			
	// 	var thisData = {title: title, name:key, len: keyArr[key], val: $('input[name="'+key+'"]').val()};
	// 	console.log(thisData);

	// 	$.ajaxSetup({
	// 	    beforeSend: function(xhr, settings) {
	//             xhr.setRequestHeader("X-CSRFToken", token);
	// 	    }
	// 	});

	// 	$.ajax({
	// 		url: '/dashboard/validation',
	// 		method: 'post',
	// 		contentType:'application/json',
	// 		data: JSON.stringify(thisData),
	// 		success: function(serverResponse){
	// 			$('input[name="'+key+'"]').siblings('.showErr').html(serverResponse);
	// 		}
	// 	});
	// }
	// $('.validate').on('keyup',function(){
	// 	var key = $(this).attr('name');
	// 	var title = $(this).parent().parent().attr('name');
	// 	validation(key, title);
	// 	var html = '';
	// 	$('form[name="'+title+'"]').children().children('.showErr').each(function(){
	// 		html += $(this).text();
	// 		return html;
	// 	}) 
	// 	if (html === ''){
	// 		$('form[name="'+title+'"]').children('.submit').removeAttr('disabled');
	// 	}
	// });
	
})