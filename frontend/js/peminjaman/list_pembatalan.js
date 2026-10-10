import {cek_auth_token} from '../token/cek_token.js'

async function getPembatalanBuku(){

    const tbody = document.getElementById("dataListPembatalanBuku");

    const response = await cek_auth_token("/pembatalan")

    if(!response) return;

    const hasil = await response.json();

    if(!hasil.data || hasil.data.length === 0){

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `Load Daftar Pembatalan Buku gagal, Data tidak ada`,
            timer: 1500,
            showConfirmButton: false
        });
        
        const RowsKosong = `
            <tr id="RowsKosong">
                <td colspan="8" class="text-center text-muted py-3">
                    Belum ada data pembatalan peminjaman buku
                </td>
            </tr>
        `

        tbody.innerHTML = RowsKosong;

        return;
    }

    try{
        const htmlRows = hasil.data.map((item, index) => `
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
                <td class="align-middle"><span class="badge text-bg-danger p-2">${item.status}</span></td>
                <td class="align-middle">${
                    new Date(item.modify_at).toLocaleDateString("id-ID", {
                        day: "2-digit",
                        month: "long",
                        year: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                        second: "2-digit",
                        hour12: false
                    }).replace("pukul", "-").trim()

                } <br/> User: ${item.modify_by}</td>
            </tr>
        `).join("");

        tbody.innerHTML = htmlRows;

        Swal.fire({
            icon: "success",
            title: "Berhasil",
            text: "List pembatalan buku berhasil ter-load ke table",
            timer: 1500,
            showConfirmButton: false
        });

    } catch(error){

        const RowsKosong = `
            <tr id="RowsKosong">
                <td colspan="8" class="text-center text-muted py-3">
                    Belum ada data pembatalan peminjaman buku
                </td>
            </tr>
        `

        tbody.innerHTML = RowsKosong;

        console.error(error);

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `Load Daftar pembatalan Buku gagal, err: ${error.message}`,
        });
    }
}

getPembatalanBuku();