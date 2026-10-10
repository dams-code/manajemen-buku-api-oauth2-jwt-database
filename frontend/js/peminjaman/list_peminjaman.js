import { cek_auth_token } from "../token/cek_token.js";

async function getListPeminjamanBuku(){

    const response = await cek_auth_token("/peminjaman");

    if(!response) return;

    const hasil = await response.json();

    const tbody = document.getElementById("dataListPeminjamanBuku");

    if(!hasil.data || hasil.data.length == 0){

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `Load Daftar peminjaman Buku gagal, Data tidak ada`,
            timer: 1500,
            showConfirmButton: false
        });

        htmlRowsKosong = `
            <tr>
                <td colspan="5" class="text-center">Belum ada list peminjaman buku.</td>
            </tr>
        `
        tbody.innerHTML = htmlRowsKosong;

        return;

    } else {

        try{

            const hasilListPeminjamanBuku = hasil.data.map((item, index) => `
                <tr>
                    <td class="align-middle">${index + 1}</td>
                    <td class="align-middle text-start">${item.no_pinjam}</td>
                    <td class="align-middle text-center">${item.qty_pinjam}</td>
                    <td class="align-middle text-start">${item.nama_member}</td>
                    <td class="align-middle">${
                        new Date(item.tanggal_pinjam).toLocaleDateString("id-ID", {
                            day: "2-digit",
                            month: "long",
                            year: "numeric"
                        })
                    }</td>
                    <td class="align-middle">${
                        new Date(item.tanggal_kembali).toLocaleDateString("id-ID", {
                            day: "2-digit",
                            month: "long",
                            year: "numeric"
                        })
                    }</td>
                    <td class="align-middle"><span class="badge text-bg-success p-2">${item.status}</span></td>
                    <td class="align-middle">${
                        new Date(item.created_at).toLocaleDateString("id-ID", {
                            day: "2-digit",
                            month: "long",
                            year: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                            second: "2-digit",
                            hour12: false
                        }).replace("pukul", "-").trim()

                    } <br/> User: ${item.created_by}</td>
                    <td class="align-middle text-center">
                        <button type="button" class="btn btn-info d-flex" style="gap: 0.3rem !important;" data-bs-toggle="modal" data-bs-target="#modalpeminjaman" data-id="${item.id}" onclick="getListPeminjamanID(this)"><i class="bi bi-eye-fill"></i>Detail</button>
                    </td>
                </tr>
            `).join("");

            tbody.innerHTML = hasilListPeminjamanBuku;

            Swal.fire({
                icon: "success",
                title: "Berhasil",
                text: "List peminjaman buku berhasil ter-load ke table",
                timer: 1500,
                showConfirmButton: false
            });

        } catch(error){

            console.error("Gagal mengambil list peminjaman buku: ", error);

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `list peminjaman buku gagal ter-load ${error}`
            });
        }
    }
}

getListPeminjamanBuku();


async function getListPeminjamanID(data){
    // console.log(data.dataset.id);
    
    const id = data.dataset.id; 

    const idPinjam = document.getElementById("id");
    const noPinjam = document.getElementById("noPinjam");
    const namaMember = document.getElementById("namaMember");
    const totalPinjamBuku = document.getElementById("totalPinjamBuku");
    const tanggalPinjam = document.getElementById("tanggalPinjam");
    const tanggalKembali = document.getElementById("tanggalKembali");
    const userPembuat = document.getElementById("userPembuat");
    const tbody = document.getElementById("tbodyBukuPinjam");

    if(id){

        try{
            const response = await cek_auth_token(`/peminjaman/${id}`)

            if(!response) return;

            if(!response.ok){

                Swal.fire({
                    icon: "error",
                    title: "Gagal",
                    text: `Load peminjaman buku id ${id}`
                });

                tbody.innerHTML = `
                    <tr id="rowKosong">
                        <td colspan="4" class="text-center text-muted py-4 small">
                            Detail daftar buku yang dipinjam kosong
                        </td>
                    </tr>
                `;
                
                throw new error(`HTTP error! status: ${hasil.status}`)
            }

            const hasil = await response.json();

            idPinjam.value = id;
            noPinjam.value = hasil.data.no_pinjam;
            namaMember.value = hasil.data.nama_member;
            totalPinjamBuku.value = hasil.data.qty_pinjam;
            tanggalPinjam.value = new Date(hasil.data.tanggal_pinjam).toLocaleDateString("id-ID", {
                day: "2-digit",
                month: "long",
                year: "numeric",
            });

            tanggalKembali.value = new Date(hasil.data.tanggal_kembali).toLocaleDateString("id-ID", {
                day: "2-digit",
                month: "long",
                year: "numeric",
            });

            const htmlRows = hasil.data.details.map((item, index) => `
                <tr>
                    <td class="align-middle">
                        ${index + 1}
                    </td>
                    <td class="align-middle">
                        ${item.judul}
                    </td>
                    <td class="align-middle">
                        ${item.judul}
                    </td>
                    <td class="align-middle">
                        ${item.judul}
                    </td>
                    <td class="align-middle">
                        ${item.qty}
                    </td>
                </tr>
            `).join("");

            tbody.innerHTML = htmlRows;

            const span = document.createElement("span");

            span.innerText = hasil.data.created_by;
            span.style.fontWeight = "bold";

            const span2 = document.createElement("span");

            span2.innerText = new Date(hasil.data.created_at).toLocaleDateString("id-ID", {
                day: "2-digit",
                month: "long",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                second: "2-digit",
                hour12: false
            }).replace("pukul", "-").trim()

            userPembuat.replaceChildren();

            userPembuat.append(span, " - ", span2);

            return hasil

        } catch(error){
            console.error("Gagal mengambil data peminjaman buku: ", error);

            Swal.fire({
                icon:"error",
                title:"Load data buku gagal",
                text: `data peminjaman buku id ${id} tidak dapat di-load, ${error}`
            });

            tbody.innerHTML = `
                <tr id="rowKosong">
                    <td colspan="4" class="text-center text-muted py-4 small">
                        Detail daftar buku yang dipinjam kosong
                    </td>
                </tr>
            `;
        }
    }

}

window.getListPeminjamanID = getListPeminjamanID;

async function simpan_pengembalian_buku(){

    const id = document.getElementById("id").value;
    const getNoPinjam = document.getElementById("noPinjam").value;

    if(id && getNoPinjam){

        const noPinjam = new URLSearchParams({"no_pinjam": getNoPinjam}).toString();

        const konfirmPengembalian = await Swal.fire({
            title: `Yakin ingin mengembalikan No Pinjam Buku ${getNoPinjam} ?`,
            text: `No Pinjam Buku ${getNoPinjam} akan dikembalikan`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Ya',
            cancelButtonText: 'Batal'
        });

        if(konfirmPengembalian.isConfirmed){
            try{
                const response = await cek_auth_token(`/pengembalian/${id}?${noPinjam}`, {
                    method: "PUT"
                });

                if(!response) return;

                if(!response.ok){
                    Swal.fire({
                        icon: "error",
                        title: "Gagal",
                        text: `Proses Pengembalian Buku ${noPinjam} gagal diproses`,
                        timer: 1500,
                        showConfirmButton: false
                    });
                    
                    throw new Error(`Proses Pengembalian Buku ${noPinjam} gagal diproses`)
                }

                await Swal.fire({
                    icon: 'success',
                    title: 'Update Status Pengembalian Buku Sukses',
                    text: `No Pinjam buku ${noPinjam} berhasil dikembalikan`,
                    timer: 1300,
                    showConfirmButton: false
                });

                const elementModal = document.getElementById("modalpeminjaman");
                const modalInstance = bootstrap.Modal.getInstance(elementModal);

                if(modalInstance){
                    modalInstance.hide();
                }

                await getListPeminjamanBuku();

            } catch(error){
                console.error(error);

                Swal.fire({
                    icon: "error",
                    title: "Gagal",
                    text: `Proses Pengembalian Buku ${noPinjam} gagal diproses, err: ${error.message}`,
                });
            }
        }
    }
}

window.simpan_pengembalian_buku = simpan_pengembalian_buku;

async function batal_peminjaman_buku(){
    const id = document.getElementById("id").value;
    const getNoPinjam = document.getElementById("noPinjam").value;

    if(id && getNoPinjam){

        const noPinjam = new URLSearchParams({"no_pinjam": getNoPinjam}).toString();

        const konfirmPengembalian = await Swal.fire({
            title: `Yakin ingin membatalkan peminjaman buku dengan No Pinjam ${getNoPinjam} ?`,
            text: `No Pinjam Buku ${getNoPinjam} akan dibatalkan`,
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Ya',
            cancelButtonText: 'Tidak'
        });

        if(konfirmPengembalian.isConfirmed){
            
            try{
                const response = await cek_auth_token(`/pembatalan/${id}?${noPinjam}`, {
                    method: "PUT"
                });

                if(!response) return;

                if(!response.ok){

                    Swal.fire({
                        icon: "error",
                        title: "Gagal",
                        text: `Proses Batal Peminjaman Buku ${noPinjam} gagal diproses`,
                        timer: 1500,
                        showConfirmButton: false
                    });
                    
                    throw new Error(`Proses pembatalan peminjaman Buku ${noPinjam} gagal diproses`)
                }

                await Swal.fire({
                    icon: 'success',
                    title: 'Update Status Batal Peminjaman Buku Sukses',
                    text: `No Pinjam buku ${noPinjam} berhasil dibatalkan peminjamannya`,
                    timer: 1300,
                    showConfirmButton: false
                });

                const elementModal = document.getElementById("modalpeminjaman");
                const modalInstance = bootstrap.Modal.getInstance(elementModal);

                if(modalInstance){
                    modalInstance.hide();
                }

                await getListPeminjamanBuku();

            } catch(error){
                console.error(error);

                Swal.fire({
                    icon: "error",
                    title: "Gagal",
                    text: `Proses Batal Peminjaman Buku ${noPinjam} gagal diproses, err: ${error.message}`,
                });
            }
        }
    }
}

window.batal_peminjaman_buku = batal_peminjaman_buku;

