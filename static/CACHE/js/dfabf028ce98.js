$(function(){$("#fileupload").fileupload({autoUpload:true,beforeSend:null});$("#fileupload").fileupload("option","redirect",window.location.href.replace(/\/[^\/]*$/,"/cors/result.html?%s"));$("#fileupload").each(function(){var a=this;$.getJSON(this.action,function(b){if(b&&b.length){$(a).fileupload("option","done").call(a,null,{result:b})}})})});
$(document).ready(function(){$("#folder_permissions").click(function(a){a.preventDefault();$("#folder_permissions_dialog").modal()});$("#mkdir").click(function(a){a.preventDefault();$("#mkdir_dialog").modal()});$("#permission_scheme").change(function(){var a=$("#permission_scheme option:selected").text();$(".permission_options").hide();if(a=="Public"){$("#permission_options_public").show()}if(a=="Futurice SSO"){$("#permission_options_sso").show()}if(a=="Static account"){$("#permission_options_static").show()}}).change();$("#mkdir_form").bind("keypress",function(a){if(a.keyCode==13){$("#mkdir_save_changes").click();return false}});$("#permissions_form").bind("keypress",function(a){if(a.keyCode==13){$("#permissions_save_changes").click();return false}});$("#password").change(function(){var a=$(this).val();console.log($(this));if(a.length<5){$("label[for='password']").html("Password (minimum 5 characters)");$("#permissions_save_changes").addClass("disabled")}else{$("label[for='password']").html("Password (ok)");$("#permissions_save_changes").removeClass("disabled")}}).change();$("#username").change(function(){var a=$(this).val();if(a.length<3){$("label[for='username']").html("Username (minimum 3 characters)");$("#permissions_save_changes").addClass("disabled")}else{$("label[for='username']").html("Username (ok)");$("#permissions_save_changes").removeClass("disabled")}}).change();$("#permissions_save_changes").click(function(a){a.preventDefault();$.ajax({type:"POST",data:$("#permissions_form").serialize(),url:permissions_post_url,success:function(){$("#folder_permissions_dialog").modal("hide");$("#notify-messages").append(permissions_message)}})});$("#mkdir_save_changes").click(function(a){a.preventDefault();$.ajax({type:"POST",data:$("#mkdir_form").serialize(),url:mkdir_post_url,success:function(b){$("#mkdir_dialog").modal("hide");if(b.success){window.location.href=b.redirect;$("#notify-messages").append(folder_message_ok)}else{$("#notify-messages").append(folder_message_fail)}},dataType:"json"})})});