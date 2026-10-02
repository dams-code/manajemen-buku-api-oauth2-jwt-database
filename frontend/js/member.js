
async function getMember(){

    const dataMember = await cek_auth_token("/member");

    if(!dataMember) return;

    const hasil = await dataMember.json();

    tbody = document.getElementById("dataMember");

    const user = await cek_auth_token("/user/aktif");
    const hasil_user = await user.json();

    const admin = hasil_user.data_user.role_ref.roledesc === "admin";;

    if(!hasil.data || hasil.data.length === 0){
        
        if (admin){
            btnTambahMember.style.display = "inline-block";

        } else {
            btnTambahMember.style.display = "none";
        }

        htmlRowKosong = `
            <tr>
                <td colspan="4" class="text-center">Tidak ada data member</td>
            </tr>
        `;

        tbody.innerHTML = htmlRowKosong;

        return;

    } else {
        try{

            if (admin){
                btnTambahMember.style.display = "inline-block";

            } else {
                btnTambahMember.style.display = "none";
            }
            
            const htmlRows = hasil.data.map((item, index) => `
                <tr>
                    <td class="align-middle">${index + 1}</td>
                    <td class="align-middle text-start">${item.nama}</td>
                    <td class="align-middle text-start">${item.alamat}</td>
                    <td class="align-middle">${item.no_telp}</td>
                    <td class="align-middle">
                        <span id="spnStatusMember_${item.id}" class="badge py-2 px-3 rounded-pill ${item.status ? "text-bg-success" : "text-bg-danger"}">
                            ${item.status ? "Aktif" : "Tidak aktif"}
                        </span>
                    </td>
                    ${admin ? `
                        <td class="d-flex gap-3 justify-content-center">
                            <button class="btn btn-primary d-flex col-gap-3" type="button" data-bs-toggle="modal" data-bs-target="#modalmember" data-id=${item.id} onclick="getDataMemberID(this);"><i class="bi bi-pencil"></i> Update</button>
                            <button class="btn btn-outline-danger d-flex col-gap-3" data-id=${item.id} type="button" onclick="hapusMember(this);"><i class="bi bi-trash-fill"></i> Hapus</button>
                        </td>` : `<td class="align-middle"><span>&nbsp;</span></td>`
                    }
                    

                    <td class="align-middle px-4 text-center">
                        ${admin ?
                            `
                                <div class="form-check form-switch d-flex align-items-center gap-2 justify-content-center">
                                    <input
                                        class="form-check-input status-switch"
                                        type="checkbox"
                                        role="switch"
                                        id="switchStatusMember_${item.id}"
                                        data-id="${item.id}"
                                        ${item.status ? "checked" : ""}
                                        onchange=(updateStatusMember(this))
                                    >
                                    <label class="form-check-label text-muted small ${item.status ? "text-success fw-bold" : "text-danger fw-bold"}" for="switchStatusMember_${item.id}" id="lblStatusMember_${item.id}">
                                        ${item.status ? "Aktif" : "Tidak aktif"}
                                    </label>
                                </div>
                            ` : `<span>&nbsp;</span>`
                        }
                        
                    </td>
                </tr>

            `).join("");

            tbody.innerHTML = htmlRows;

        } catch(error){
            console.log("Gagal mengambil data member: ", error);

            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: `Data member gagal ter-load ${error}`
            });
        }
    }
}

getMember();


async function updateStatusMember(data){
    const id = parseInt(data.dataset.id)
    const cekSwitch = data.checked;

    const lblStatusMember = document.getElementById(`lblStatusMember_${id}`);

    const spnStatusMember = document.getElementById(`spnStatusMember_${id}`); 

    data.disabled = true;

    try{
        const response = await cek_auth_token(`/member/${id}?status_member=${cekSwitch}`, {
            method: 'PATCH'
        });

        if(!response) return;

        if(!response.ok){
            throw new Error(`Gagal mengganti status member id ${id}`)
        }

        if(cekSwitch){

            lblStatusMember.textContent = "Aktif";
            lblStatusMember.className = "form-check-label small text-success fw-bold";

            spnStatusMember.innerHTML = "Aktif"
            spnStatusMember.className = "badge py-2 px-3 rounded-pill text-bg-success"
        } else {
            lblStatusMember.textContent = "Tidak aktif";
            lblStatusMember.className = "form-check-label small text-danger fw-bold";

            spnStatusMember.innerHTML = "Tidak aktif"
            spnStatusMember.className = "badge py-2 px-3 rounded-pill text-bg-danger"
        }

    }catch(error){
        data.checked = !cekSwitch;

        Swal.fire({
            icon: "error",
            title: "Gagal",
            text: `Gagal mengganti status member id ${id}`,
        });

    }finally{
        data.disabled = false;
    }
}