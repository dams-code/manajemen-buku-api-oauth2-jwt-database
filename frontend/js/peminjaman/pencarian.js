
import { cek_auth_token } from "../token/cek_token.js";

const cariMember = document.getElementById("cariMember");
const dropDownListNamaMember = document.getElementById("dropDownListNamaMember");
const alertHasil = document.getElementById("hasil-cari-nama-member");

let queryPencarianMember;

function showAlertMember(data){
    const namaMember = document.getElementById("namaMember");
    const namaMemberInfo = document.getElementById("namaMemberInfo");
    const alamatMemberInfo = document.getElementById("alamatMemberInfo");
    const notelpMemberInfo = document.getElementById("notelpMemberInfo");
    const statusMemberInfo = document.getElementById("statusMemberInfo");
    
    namaMember.innerText = `${data.id} - ${data.nama}`;

    namaMemberInfo.innerHTML = data.nama;
    alamatMemberInfo.innerHTML = data.alamat;
    notelpMemberInfo.innerHTML = data.no_telp;
    statusMemberInfo.innerHTML = data.status ? "Aktif" : "Tidak Aktif";

    alertHasil.style.display = "grid";
    alertHasil.className="row-gap-2 p-3";

    setTimeout(() => {
        alertHasil.style.opacity = "1";
        alertHasil.style.transform = "translateY(0)";
    }, 10);
}

function hideAlertMember(){
    alertHasil.style.opacity = "0";
    alertHasil.style.transform = "translateY(-8px)";

    setTimeout(() => {
        alertHasil.style.display = "none";
    }, 400);
}

cariMember.addEventListener("input", async function(event){

    if(!event.target.value.trim()){
        hideAlertMember();
        dropDownListNamaMember.innerHTML = "";
        dropDownListNamaMember.style.display = "none";

        return;
    }

    const text = event.target.value.trim();

    clearTimeout(this.queryPencarianMember);

    queryPencarianMember = setTimeout(async () => {
        if (text.length === 0){
            console.warn("Input Id / Nama kosong");
        }

        let url = "/member?";

            if(!isNaN(text) && text !== ""){
                url += `id=${encodeURIComponent(text)}`;
            } else {
                url += `nama=${encodeURIComponent(text)}`;
            }

        try{
            const response = await cek_auth_token(url)
            const hasil = await response.json();
            const hasil_cari_member = hasil.data;

            dropDownListNamaMember.innerHTML = "";

            // console.log(hasil_cari_member);

            if(Array.isArray(hasil_cari_member) && hasil_cari_member.length > 0){
                
                dropDownListNamaMember.style.display = "block";
                
                hasil_cari_member.forEach(member => {
                    if(member.status == true){
                        const li = document.createElement("li");
                        li.className = "list-group-item list-group-item-action cursor-pointer py-2";
                        li.innerText = `ID: ${member.id} ${member.nama}`;

                        li.onclick = function(){
                            // namaMember.innerText = member.nama;
                            showAlertMember(member);
                            cariMember.value = member.nama;
                            dropDownListNamaMember.innerHTML = "";
                            dropDownListNamaMember.style.display = "none";
                        };

                        dropDownListNamaMember.appendChild(li);
                    }
                });
            } else {
                dropDownListNamaMember.style.display = "block";
                dropDownListNamaMember.innerHTML = `<div class="list-group-item text-muted">Member tidak ditemukan</div>`;
            }

        } catch(error){
            console.error(error);
        }

    }, 200);
});


