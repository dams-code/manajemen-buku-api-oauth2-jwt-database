async function logout(){
    
    const get_token = localStorage.getItem("access_token");
    
    if(!get_token){
        window.location.replace("/login.html")
        return;
    }

    const confirmModal = await Swal.fire({
        title: "Apakah anda yakin ingin logout?",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Ya, Logout!',
        cancelButtonText: 'Batal'
    });

    if (!confirmModal.isConfirmed) return;

    try{
        const response = await fetch("/logout", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${get_token}`
            }
        });

        localStorage.removeItem("access_token");

        await Swal.fire({
            icon: "success",
            title: "Logout berhasil",
            text: "Anda sudah logout",
            timer: 2000,
            showConfirmButton: false
        });

        window.location.replace("/login.html");
    } catch(error){
        console.error("Error logout:", error);

        localStorage.removeItem("access_token");
        window.location.replace("/login.html");
    }
}