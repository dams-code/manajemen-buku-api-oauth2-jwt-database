(async function(){
    const data_user = await cek_auth_token(`/user/aktif`)

    if (!data_user) return;

    const hasil =  await data_user.json();
    const userAktif = document.getElementById("userAktif");
    const userRoleAktif = document.getElementById("userRoleAktif");

    if (hasil){
        console.log(hasil.data_user);

        userAktif.textContent = hasil.data_user.username;
        userRoleAktif.textContent = hasil.data_user.role;
    }

})();