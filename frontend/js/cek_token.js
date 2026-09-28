(function(){
    const token = localStorage.getItem("access_token");

    const pathUrlAKtif = window.location.pathname;

    if(!token && !pathUrlAKtif.includes('login.html')){
        window.location.replace("/login.html");
    }

    if(token && pathUrlAKtif.includes('login.html')){
        window.location.replace("/");
    }
})();

// cek expired token
// cek_token berlaku diseluruh crud buku
async function cek_auth_token(url, options={}){
    const token = localStorage.getItem('access_token');

    if(!token){
        window.location.replace("/login.html");
        return;
    }

    options.headers ={
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    }

    try{
        const response = await fetch(url, options);

        if (response.status === 403){
            const result = await response.json();
            const pesanError = result.detail || result.pesan || "Akses halaman ditolak";
            
            // console.error(`Error (${response.status}):`, pesanError);

            window.location.replace("/403.html");
            
            return null;
        }

        if (response.status === 401){
            localStorage.removeItem("access_token");

            await Swal.fire({
                icon: "warning",
                title: "Sesi login berakhir",
                text: "Sesi login anda habis, Silahkan login kembali",
                confirmButtonText: 'OK',
                allowOutsideClick: false
            });

            window.location.replace("/login.html")
            return;
        }

        return response;
    } catch(error){
        console.error('Error cek auth token :  ', error);
        throw error;
    }
}