function onSignIn(googleUser) {
    var profile=googleUser.getBasicProfile();
    $(".g-signin2").css("display", "none");
    $("#profile").css("display","block");
    $("#usericon").attr('src', profile.getImageUrl());
    $("#emailAdd").text(profile.getEmail());
    $("#name").text(profile.getName());
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
}

function signOut(){
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function(){
        $('.g-signin2').css("display","block");
        $('.profile').css("display","none");
    });
}

function renderButton() {
    gapi.signin2.render('g-signin2', {
      'scope': 'profile email',
      'width': 240,
      'height': 50,
      'longtitle': true,
      'theme': 'dark',
      'onsuccess': onSuccess,
      'onfailure': onFailure
    });
}

