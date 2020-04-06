const btnDelete = document.querySelectorAll('.btn-delete') /* Devuelve una lista */

if(btnDelete){
    /* Recorrer la lista de btnDelete */
    const btnArray = Array.from(btnDelete);
    /* foreach para recorrer */
    btnArray.forEach((btn) => {
        /* event de escucha */
        btn.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to delete it?')) {
                /* Cancelar */
                e.preventDefault();
            }
        });
    });
}