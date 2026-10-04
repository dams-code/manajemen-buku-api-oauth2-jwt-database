
const username = document.getElementById('username');
const password = document.getElementById('password');

async function loginUser(e){

    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }

    if (!username.value || !password.value) {
        Swal.fire({
            icon: 'error',
            title: 'Login Gagal',
            text: 'Username dan Password wajib diisi!',
        });
        return;
    }

    try {

        const formDataUser = new URLSearchParams();

        formDataUser.append('username', username.value);
        formDataUser.append('password', password.value);

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formDataUser
        });

        const result_formData = await response.json();

        if(response.ok){
            const get_token = result_formData.access_token || result_formData.data_token?.access_token;
            localStorage.setItem('access_token', get_token);
            
            Swal.fire({
                icon: 'success',
                title: 'Login Berhasil',
                text: `Anda dengan username ${username.value} berhasil login!`,
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                window.location.href = '/';
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Login Gagal',
                text: result_formData.detail || 'Username atau Password salah!',
            });
        }

    } catch (error) {
        console.error('Error saat login:', error);
        Swal.fire({
            icon: 'error',
            title: 'Login Gagal',
            text: "Terjadi kesalahan saat mencoba login. Silakan coba lagi.",
        });
    }
}