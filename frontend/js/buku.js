
async function getBuku(){

    const data_buku = await cek_auth_token("/buku");

    if (!data_buku) return;

    const hasil = await data_buku.json();

    const tbody = document.getElementById("dataBuku")

    // console.log(hasil)

    const user = await cek_auth_token(`/user/aktif`);
    const hasil_user = await user.json();
    const cekManajer = hasil_user.data_user.role === "manajer";

    if (!hasil.data || hasil.data.length === 0){
        
        const btnTambahBuku = document.getElementById("btnTambahBuku");
            
        if (cekManajer){
            btnTambahBuku.style.display = "none";
        } else {
            btnTambahBuku.style.display = "inline-block";
        }

        htmlRowsKosong = `
            <tr>
                <td colspan="5" class="text-center">Belum ada data buku. Silakan tambah buku baru.</td>
            </tr>
        `
        tbody.innerHTML = htmlRowsKosong

        return;
    } else {
        try{
            // console.log(cekManajer);

            console.log(hasil_user.data_user.role_ref.roledesc);

            const htmlRows = hasil.data.map((item, index) => `
                <tr>
                    <td class="align-middle">${index + 1}</td>
                    <td class="align-middle text-start">${item.judul}</td>
                    <td class="align-middle text-start">${item.penulis}</td>
                    <td class="align-middle">${item.tahun}</td>
                    <td class="align-middle">${item.qty}</td>
                    <td class="align-middle">${item.genre}</td>
                    <td class="align-middle">
                        <span id="spnStatusBuku_${item.id}" class="badge py-2 px-3 rounded-pill ${item.tersedia ? "text-bg-success" : "text-bg-danger"}">
                            ${item.tersedia ? "Tersedia" : "Tidak tersedia"}
                        </span>
                    </td>
                    ${!cekManajer ? `
                        <td class="d-flex gap-3 justify-content-center">
                            <button class="btn btn-primary d-flex col-gap-3" type="button" data-bs-toggle="modal" data-bs-target="#modalbuku" data-id=${item.id} onclick="getDataBukuID(this);"><i class="bi bi-pencil"></i> Update</button>
                            <button class="btn btn-outline-danger d-flex col-gap-3" data-id=${item.id} type="button" onclick="hapusBuku(this);"><i class="bi bi-trash-fill"></i> Hapus</button>
                        </td>` : `<td class="align-middle"><span>&nbsp;</span></td>`
                    }
                    

                    <td class="align-middle px-4 text-center">
                        ${!cekManajer ?
                            `
                                <div class="form-check form-switch d-flex align-items-center gap-2 justify-content-center">
                                    <input
                                        class="form-check-input status-switch"
                                        type="checkbox"
                                        role="switch"
                                        id="switchStatusBuku_${item.id}"
                                        data-id="${item.id}"
                                        ${item.tersedia ? "checked" : ""}
                                        onchange=(updateStatusBuku(this))
                                    >
                                    <label class="form-check-label text-muted small ${item.tersedia ? "text-success fw-bold" : "text-danger fw-bold"}" for="switchStatusBuku" id="lblStatusBuku_${item.id}">
                                        ${item.tersedia ? "Tersedia" : "Tidak tersedia"}
                                    </label>
                                </div>
                            ` : `<span>&nbsp;</span>`
                        }
                        
                    </td>
                </tr>
            `).join("");
            
            // console.log(hasil_user)

            const btnTambahBuku = document.getElementById("btnTambahBuku");
            
            if (cekManajer){
                btnTambahBuku.style.display = "none";
            } else {
                btnTambahBuku.style.display = "inline-block";
            }

            tbody.innerHTML = htmlRows

            Swal.fire({
                icon: "success",
                title: "Berhasil",
                text: "Data buku berhasil ter-load ke table",
                timer: 1500,
                showConfirmButton: false
            });

        } catch(error){
            console.error("Gagal mengambil data buku: ", error);

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `Data buku gagal ter-load ${error}`
            })
        }
    }
}

getBuku();

async function getDataBukuID(data){
    document.getElementById("modalJudul").innerText = "Update Buku";

    const hideId = document.getElementById("hide-id-tambah-buku");
    
    hideId.style.display = "flex";

    document.getElementById("id").disabled = true;

    const id = parseInt(data.dataset.id, 10)
    const id_input = document.getElementById("id")
    const judul = document.getElementById("judul")
    const penulis = document.getElementById("penulis")
    const tahun = document.getElementById("tahun")
    const qty = document.getElementById("qty")
    const list_genre = document.getElementById("list_genre")
    const list_tersedia = document.getElementById("list_tersedia")


    if (id){
        try{
            const data_buku = await cek_auth_token(`/buku/${id}`);

            if(!data_buku) return;

            // if (data_buku.status == 401) {
            //     localStorage.removeItem("access_token");

            //     window.location.replace("/login.html");
            // }

            if (!data_buku.ok){

                Swal.fire({
                    icon:"error",
                    title:"Load data buku berdasarkan ID gagal",
                    text: `Buku id ${id} tidak dapat ditemukan`
                });

                throw new error(`HTTP error! status: ${data_buku.status}`)
            }

            const result = await data_buku.json()

            // console.log(result.data)

            id_input.value = result.data.id
            judul.value = result.data.judul
            penulis.value = result.data.penulis
            tahun.value = result.data.tahun
            qty.value = result.data.qty
            list_genre.value = result.data.genre
            list_tersedia.value = result.data.tersedia

            return result
        } catch(error){
            console.error("Gagal mengambil data buku: ", error)

            Swal.fire({
                icon:"error",
                title:"Load data buku gagal",
                text: `Buku id ${id} tidak dapat di-load, ${error}`
            });
        }
    }
}

async function simpan_buku(){
    const idVal = document.getElementById("id").value;
    const tahunVal = document.getElementById("tahun").value;
    // console.log("cek id buku : ", idVal)

    // console.log("cek id buku : ", idVal ? 'ada': 'tidak ada')

    // const test = idVal ? parseInt(idVal, 10) : null;

    // console.log(test ? "PUT" : "POST");

    if(!tahunVal || tahunVal.length !== 4){
        Swal.fire({
            icon:"warning",
            title: "Input tahun tidak valid",
            text: "Tahun wajib maksimal 4 digit angka!",
            showConfirmButton: false,
            timer: 1500
        });
        return;
    }

    const data_buku = {
        judul: document.getElementById("judul").value,
        penulis: document.getElementById("penulis").value,
        // tahun: parseInt(document.getElementById("tahun").value, 10),
        tahun: parseInt(tahunVal, 10),
        genre: document.getElementById("list_genre").value,
        tersedia: JSON.parse(document.getElementById("list_tersedia").value),
        qty: JSON.parse(document.getElementById("qty").value)
    }

    const id = idVal ? parseInt(idVal, 10) : null;
    const url = id ? `/buku/${id}` : `/buku`
    const method = id ? "PUT" : "POST";

    try{
        const response = await cek_auth_token(url, {
            method: method,
            // headers: {
            //     "Content-Type": "application/json"
            // },
            body: JSON.stringify(data_buku)
        });

        if(!response) return;

        if(response.ok){
            await Swal.fire({
                icon: "success",
                title: "Berhasil",
                text: id ? `Buku ID ${id} berhasil diperbaharui` : "Buku baru berhasil ditambah kedalam table",
                timer: 1500,
                showConfirmButton: false            
            });

            const elementModal = document.getElementById("modalbuku")
            const modalInstance = bootstrap.Modal.getInstance(elementModal)

            if(modalInstance){
                modalInstance.hide();
            }

            await getBuku();
        } else {
            const errorDetail = await response.json();
            // console.error(errorDetail);

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `${errorDetail.pesan} | Gagal ${method} pada buku terjadi error.`
            });
        }
    } catch(error){
        console.error("Error Simpan Buku", error)

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `TIdak dapat terhubung ke FastAPI endpoint`
        });
    }

}

async function hapusBuku(data){
    const id = parseInt(data.dataset.id);

    if (!id){
        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `Buku Id ${id} tidak ditemukan!`
        });
        return;
    }

    const result = await Swal.fire({
        title: `Yakin ingin menghapus buku Id ${id} ?`,
        text: `Buku dengan Id ${id} akan dihapus permanen`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Ya, hapus!',
        cancelButtonText: 'Batal'
    });

    if (result.isConfirmed){
        try{
            const response = await cek_auth_token(`/buku/${id}`, {
                method: "DELETE"
            });

            if(!response) return;

            if(response.ok){
                await Swal.fire({
                    icon: 'success',
                    title: 'Terhapus',
                    text: `Data buku Id ${id} berhasil terhapus`,
                    timer: 1500,
                    showConfirmButton: false
                });

                await getBuku();
            }else {
                const errorDetail = await response.json();

                Swal.fire({
                    icon: 'error',
                    title: 'Gagal hapus buku',
                    text: `${errorDetail.detail} | Buku id ${id} Gagal dihapus.`
                });
            }
        } catch(error){
            console.error("Gagal menghapus buku: ", error);

            Swal.fire({
                icon: "error",
                title: "Error akses",
                text: "Gagal terhubung ke Fast API Endpoint"
            });
        }
    }
}

function setTambahBuku(){
    document.getElementById("modalJudul").innerText = "Tambah Buku";

    const id = document.getElementById("id");
    const hideId = document.getElementById("hide-id-tambah-buku");
    
    id.removeAttribute('disabled');
    id.value = "";
    hideId.style.display = "none";
    document.getElementById("judul").value = "";
    document.getElementById("penulis").value = "";
    document.getElementById("tahun").value = "";
    document.getElementById("qty").value = "";
    document.getElementById("list_genre").value = "";
    document.getElementById("list_tersedia").value = "true";
}

async function updateStatusBuku(data){
    const id = parseInt(data.dataset.id)
    const cekSwitch = data.checked;

    const lblStatusBuku = document.getElementById(`lblStatusBuku_${id}`);

    const spnStatusBuku = document.getElementById(`spnStatusBuku_${id}`); 

    data.disabled = true;

    try{
        const response = await cek_auth_token(`/buku/${id}?tersedia=${cekSwitch}`, {
            method: 'PATCH'
        });

        if(!response) return;

        if(!response.ok){
            throw new Error(`Gagal mengganti status buku id ${id}`)
        }

        if(cekSwitch){

            lblStatusBuku.textContent = "Tersedia";
            lblStatusBuku.className = "form-check-label small text-success fw-bold";

            spnStatusBuku.innerHTML = "Tersedia"
            spnStatusBuku.className = "badge py-2 px-3 rounded-pill text-bg-success"
        } else {
            lblStatusBuku.textContent = "Tidak tersedia";
            lblStatusBuku.className = "form-check-label small text-danger fw-bold";
            
            spnStatusBuku.innerHTML = "Tidak tersedia"
            spnStatusBuku.className = "badge py-2 px-3 rounded-pill text-bg-danger"
        }

    }catch(error){
        data.checked = !cekSwitch;
        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `Gagal mengganti status buku id ${id}`,
        });
    }finally{
        data.disabled = false;
    }
}