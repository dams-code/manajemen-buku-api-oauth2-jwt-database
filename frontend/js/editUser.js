
const username = document.getElementById("username");
const nama = document.getElementById("nama");
const list_role = document.getElementById("list_role");

async function getUserID() {
    try{

        const data_user =  await cek_auth_token("/user/aktif");

        if(!data_user) return;

        if (!data_user.ok){
            Swal.fire({
                icon:"error",
                title:"Load data user gagal",
                text: `Username ${username.value} tidak ditemukan`
            });

            throw new error("Gagal mengambil username");
        }

        const result = await data_user.json();

        username.value = result.data_user.username;
        nama.value = result.data_user.nama;
        list_role.value = result.data_user.role;

        return result;

    } catch(error){
        console.error("Gagal mengambil data user: ", error)

        Swal.fire({
            icon:"error",
            title:"Load data user gagal",
            text: `Username ${username.value} tidak dapat di-load, ${error}`
        });
    }
    
};

getUserID();

async function updateUser(e){

    if(e){
        e.preventDefault();
        e.stopPropagation();
    }

    try{

        const update_data_user = {
            nama: nama.value,
            role: list_role.value
        }

        // console.log(username.value);

        const response_update = await cek_auth_token(`/user/aktif/update/${username.value}`, {
            method: "PUT",
            body: JSON.stringify(update_data_user)
        });

        if(!response_update) return;

        // console.log(response_update);

        if(response_update.ok){
            await Swal.fire({
                icon: "success",
                title: "Berhasil",
                text: `Data Username ${username.value} berhasil update`,
                timer: 1500,
                showConfirmButton: false            
            });
        } else {
            const errorDetail = await response_update.json();

            console.log(errorDetail.detail);

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `${errorDetail.detail} | Gagal update user terjadi error.`
            });
            return;
        }

    } catch(error){
        console.error("Error Update User", error)

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `TIdak dapat terhubung ke FastAPI endpoint`
        });
    }
}