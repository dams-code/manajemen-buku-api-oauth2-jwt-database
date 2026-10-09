import {cek_auth_token} from '../token/cek_token.js'

async function getPengembalianBuku(){
    try{
        const response = await cek_auth_token("/pengembalian")

        if(!response) return;

        if(!response.ok){

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `Load Daftar Pengembalian Buku gagal`,
                timer: 1500,
                showConfirmButton: false
            });
            
            throw new Error(`Load Daftar Pengembalian Buku gagal`)
        }

        const hasil = await response.json();

        const tbody = document.getElementById("dataListPengembalianBuku");

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
                <td class="align-middle"><span class="badge text-bg-primary p-2">${item.status}</span></td>
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
            text: "List pengembalian buku berhasil ter-load ke table",
            timer: 1500,
            showConfirmButton: false
        });

    } catch(error){

        console.error(error);

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `Load Daftar Pengembalian Buku gagal, err: ${error.message}`,
        });
    }
}

getPengembalianBuku();