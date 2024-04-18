import axiosInstance from '../AxiosInstance'; 
const deleteItemService = async (item_id) => {
    const validbuyerid = { 
        seller_product_id:item_id
    }
    try {
        const response = await axiosInstance.delete(`/shopping_cart/me/${validbuyerid.seller_product_id}`,validbuyerid.seller_product_id );
        console.log('Se ha eliminado el item con éxito:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error al eliminar el item:', error);
        throw error;
    }
};
const getCartItems = async () => {
    
    try {
        const response = await axiosInstance.get('/shopping_cart/me');
        console.log('Los productos del carrito son:', response);
        return response.data;
    } catch (error) {
        console.error('Error al recuperar productos del carrito:', error);
        throw error;
    }
};
const getSellerProduct = async (productId) => {
    try {
        const response = await getSellerProduct(productId);
        console.log('Los productos del carrito son:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error al obtener información del producto:', error);
        throw error;
    }
};


export {getSellerProduct,deleteItemService,getCartItems};