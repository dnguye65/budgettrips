function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    $(".g-signin2").css("display", "none");
    $(".profile").css("display","block");
    $("#usericon").attr('src', profile,getImageUrl());
    $("#emailAdd").text(profile.getEmail());
    console.log('Name: ' + profile.getName());
  }