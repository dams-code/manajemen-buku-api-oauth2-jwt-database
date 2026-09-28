

async function getUser(){

    const getUser = await cek_auth_token("/users")

    if (!getUser) return;

    const tbody = document.getElementById("dataUser");

    listUser = await getUser.json();

    if (listUser && listUser.length === 0) {
        
        htmlKosong = `
            <tr>
                <td colspan="5" class="text-center">Belum ada data buku. Silakan tambah buku baru.</td>
            </tr>
        `

        tbody.innerHTML = htmlRows;
    }
    else {
        try{
            // console.log(user);
            const user = await cek_auth_token("/user/aktif");
            const hasil_user = await user.json();

            // console.log(hasil_user);

            const cekManajer = hasil_user.data_user.role === "manajer";

            if (cekManajer){
                const htmlRows = listUser.data_user.map((user) => `
                    <tr>
                        <td class="align-middle">${user.id}</td>
                        <td class="align-middle">${user.username}</td>
                        <td class="align-middle">${user.nama}</td>
                        <td class="align-middle">${user.role}</td>
                        ${cekManajer ? `
                            <td class="d-flex gap-3 justify-content-center">
                                <button class="btn btn-primary d-flex col-gap-3" type="button" data-bs-toggle="modal" data-bs-target="#modaluser" data-username=${user.username} data-id=${user.id} onclick="getDataUserID(this);"><i class="bi bi-pencil"></i> Update</button>
                                <button class="btn btn-outline-danger d-flex col-gap-3" data-username=${user.username} type="button" onclick="hapusUser(this);"><i class="bi bi-trash-fill"></i> Hapus</button>
                            </td>
                        ` : `<td class="align-middle"><span>&nbsp;</span></td>`}
                    </tr>
                `).join("");

                tbody.innerHTML = htmlRows;

                const btnTambahUser = document.getElementById("btnTambahUser");
                

                console.log("cek manajer : ", cekManajer);

                if(cekManajer){
                    btnTambahUser.style.display = "inline-block";
                } else {
                    btnTambahUser.style.display = "none";
                }

                Swal.fire({
                    icon: "success",
                    title: "Berhasil",
                    text: "Data User berhasil ter-load ke table",
                    timer: 1100,
                    showConfirmButton: false
                });

            } else {
                htmlKosong = `
                    <tr>
                        <td colspan="5" class="text-center bg-danger text-white">Akses Ditolak</td>
                    </tr>
                `
                tbody.innerHTML = htmlKosong;
            }

        } catch(error){

            console.error(error);

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `Data User gagal ter-load ${error}`
            });
        }
    }

    
}

getUser();


async function simpan_user(){

    try{

        const idUser = document.getElementById("idUser").value;

        const cek_id_username = idUser ? parseInt(idUser, 10) :  null;
        
        const username = document.getElementById("username");
        const nama = document.getElementById("nama");
        const list_role = document.getElementById("list_role");
        const password = document.getElementById("password");

        const url = cek_id_username ? `/user/update/${username.value}` : "/user";
        const method = cek_id_username ? "PUT" : "POST";

        // console.log("id user",document.getElementById("idUser"));
        // console.log(url);
        // console.log(method);

        const dataUserUpdate = {
            id: cek_id_username,
            nama: nama.value,
            role: list_role.value
        }

        const dataUserCreate = {
            "username": username.value,
            "nama": nama.value,
            "password": password.value,
            "role": list_role.value,
        }

        // console.log(cek_id_username ? JSON.stringify(dataUserUpdate) : JSON.stringify(dataUserCreate));

        const response = await cek_auth_token(url, {
            method: method,
            body: cek_id_username ? JSON.stringify(dataUserUpdate) : JSON.stringify(dataUserCreate)
        });

        if(!response) return;

        if(response.ok){
            await Swal.fire({
                icon: "success",
                title: "Berhasil",
                text: cek_id_username ? `Data User ${username.value} berhasil di perbaharui` : "Registrasi / Pendaftaran User Berhasil",
                timer: 1500,
                showConfirmButton: false
            });

            const elementModal = document.getElementById("modaluser");
            const modalInstance = bootstrap.Modal.getInstance(elementModal);

            if(modalInstance){
                modalInstance.hide();
            }

            await getUser();
        } else {
            const errorDetail = await response.json();

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `${errorDetail.detail} | Gagal ${method} pada tambah user terjadi error`
            });
        }
    } catch(error){
        console.error(error);

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `TIdak dapat terhubung ke FastAPI endpoint`
        });
    }
}

function setTambahUser(){
    document.getElementById("modalJudul").innerText = "Tambah User";

    document.getElementById("form-password").style.display = "flex";

    document.getElementById("idUser").value = "";
    document.getElementById("username").value = "";
    document.getElementById("username").removeAttribute('disabled');
    document.getElementById("nama").value = "";
    document.getElementById("password").value = "";
    document.getElementById("list_role").value = "";
}

async function getDataUserID(data){
    const getIdUsername = data.dataset.id;
    const getUsername = data.dataset.username;

    // console.log(getIdUsername);
    // console.log(getUsername);

    const idUser = document.getElementById("idUser");
    const username = document.getElementById("username");
    const nama = document.getElementById("nama");
    const list_role = document.getElementById("list_role");

    // console.log(getIdUsername);

    document.getElementById("modalJudul").innerText = "Update User";
    document.getElementById("form-password").style.display = "none";
    
    if(getIdUsername){
        try{
            const data_user = await cek_auth_token(`/user/${getUsername}`)

            if(!data_user) return;

            if(!data_user.ok){
                Swal.fire({
                    icon: "error",
                    title: "Load data user berdasarkan ID gagal",
                    text: `username ${getUsername} tidak ditemukan`
                });

                throw new error(`Http error, status: ${data_user.status}`);
            }

            const result = await data_user.json();

            idUser.value = result.data_user.id;
            username.value = getUsername;
            nama.value = result.data_user.nama;
            list_role.value = result.data_user.role;

            return result;

        } catch(error){
            console.error("Gagal mengambil data user : ", error);

            Swal.fire({
                icon:"error",
                title:"Load data user gagal",
                text: `Data Username ${getUsername} tidak dapat di-load, ${error}`
            });
        }
    }
}


async function hapusUser(data){

    const getUsername = data.dataset.username;

    const result = await Swal.fire({
        title: `Yakin ingin menghapus user ${getUsername} ?`,
        text: `User ${getUsername} akan dihapus permanen`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Ya, hapus!',
        cancelButtonText: 'Batal'
    });

    if(result.isConfirmed){
        try{
            const response_delete_user = await cek_auth_token(`/user/${getUsername}`, {
                method: "DELETE"
            });

            if(!response_delete_user) return;

            if(response_delete_user.ok){
                await Swal.fire({
                    icon: 'success',
                    title: 'Terhapus',
                    text: `Data User ${getUsername} berhasil terhapus`,
                    timer: 1500,
                    showConfirmButton: false
                });

                await getUser();
            } else {
                const errorDetail = await response_delete_user.json();

                Swal.fire({
                    icon: 'error',
                    title: 'Gagal hapus user',
                    text: `${errorDetail.pesan} | User ${getUsername} Gagal dihapus.`
                });
            }
        } catch(error){
            console.error(error);
        }
    }

    

}