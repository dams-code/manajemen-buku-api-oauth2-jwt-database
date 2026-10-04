
const username = document.getElementById("username").value.trim();

const nama = document.getElementById("nama");
const role = document.getElementById("list_role");
const password = document.getElementById("password");
const conf_password = document.getElementById("conf_password");

function cekFormatUsername(username){
    const setRegex = /^[a-zA-Z0-9_-]+$/;

    return setRegex.test(username);
}

async function registrasiUser(e){
    if(e){
        e.preventDefault();
        e.stopPropagation();
    }

    if(!cekFormatUsername(username)) {
        Swal.fire({
            icon: "error",
            title: "Gagal Registrasi",
            text: "Username tidak boleh mengandung spasi atau karakter spesial seperti ' atau \""
        });

        console.log(cekFormatUsername(username))

        return;
    }

    // console.log(password.value)
    // console.log(conf_password.value)

    if (password.value !== conf_password.value) {
        Swal.fire({
            icon: "error",
            title: "Gagal Registrasi",
            text: "Password dan Konfirmasi Password tidak sama"
        });

        return;
    }

    const formRegistrasiUser = {
        "username": username,
        "nama": nama.value,
        "role_id": role.value,
        "password": conf_password.value,
    }

    try{
        const response = await fetch("/registrasi", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formRegistrasiUser)
        });

        const result_registrasi = await response.json();

        if (result_registrasi.status == 400){
            Swal.fire({
                icon: 'error',
                title: 'Registrasi Gagal',
                text: `${result_registrasi.pesan}`,
            });
            return;
        }

        if (response.ok || result_registrasi.status == 400){
            Swal.fire({
                icon: "success",
                title: "Registrasi Berhasil",
                text: "Registrasi User Berhasil, Silahkan Login Kembali",
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                window.location.href="/login.html"
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Registrasi Gagal',
                text: result_registrasi.detail || 'Terjadi kesalahan registrasi user',
            });
        }
    } catch(error){
        console.error(error);

        Swal.fire({
            icon: 'error',
            title: 'Registrasi Gagal',
            text: "Terjadi kesalahan saat registrasi. Silakan coba lagi.",
        });
    }

}
