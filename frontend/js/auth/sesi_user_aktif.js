import { cek_auth_token } from "../token/cek_token.js";

(async function(){
    const data_user = await cek_auth_token(`/user/aktif`)

    if (!data_user) return;

    const hasil =  await data_user.json();
    const userAktif = document.getElementById("userAktif");
    const userRoleAktif = document.getElementById("userRoleAktif");

    if (hasil){
        console.log(hasil.data_user);
        const roleName = hasil.data_user?.role_ref?.roledesc;

        console.log(roleName)

        userAktif.textContent = hasil.data_user.username;
        userRoleAktif.textContent = hasil.data_user.role_ref.roledesc;
        
    }

})();