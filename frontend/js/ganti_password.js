
const username = document.getElementById("username");
const passwordLama = document.getElementById("passwordLama");
const passwordBaru = document.getElementById("passwordBaru");

async function getUsername(){

    try{
        const response_username = await cek_auth_token("/user/aktif");

        if(!response_username) return;

        if(!response_username.ok){
            Swal.fire({
                icon:"error",
                title:"Load data user gagal",
                text: `Username ${username.value} tidak ditemukan`
            });

            throw new error("Gagal mengambil username");
        }

        const result = await response_username.json();

        username.value = result.data_user.username;

        return result;

    } catch(error){
        console.error("Gagal mengambil data user: ", error)

        Swal.fire({
            icon:"error",
            title:"Load data user gagal",
            text: `Username ${username.value} tidak dapat di-load, ${error}`
        });
    }
}

getUsername();

async function gantiPasswordUser(e){


    if (e){
        e.preventDefault();
        e.stopPropagation();
    }

    const set_data_password = {
        passwordLama: passwordLama.value,
        passwordBaru: passwordBaru.value
    } 

    try{
        const response_update_password = await cek_auth_token(`/user/update/password/${username.value}`, {
            method: "PUT",
            body: JSON.stringify(set_data_password),
        });

        if(!response_update_password) return;

        if (response_update_password.ok){
            await Swal.fire({
                icon: "success",
                title: "Update Password Berhasil",
                text: `Password user ${username.value}`,
                showConfirmButton: false,
                timer: 1500
            });
        } else {
            const errorDetail = await response_update_password.json();

            Swal.fire({
                icon: "error",
                title: "Update Password Gagal",
                text: `${errorDetail} | Terjadi error saat update password user ${username}`
            });
            return;
        }
    } catch(error){

        console.error("Error Update Password User", error)

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `TIdak dapat terhubung ke FastAPI endpoint`
        });
    }

}