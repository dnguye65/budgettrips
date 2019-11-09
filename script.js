function onSignIn(googleUser) {
    var profile=googleUser.getBasicProfile();
    $(".g-signin2").css("display", "none");
    $(".profile").css("display","block");
    $("#usericon").attr('src', profile.getImageUrl());
    $("#emailAdd").text(profile.getEmail());
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}
  }