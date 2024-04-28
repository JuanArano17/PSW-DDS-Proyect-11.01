import React, { useEffect, useState } from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Button, Box, Container, Grid, TablePagination, Typography } from '@mui/material';
import { getPendingProducts } from '../api/services/products/AdminService';
import styles from '../styles/styles';
import TopBar from '../components/topbar/TopBar';
import Footer from '../components/footer/Footer';
import { useHistory } from 'react-router-dom';

const AdminPage = () => {
    const [products, setProducts] = useState([]);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const history = useHistory();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await getPendingProducts();
                console.log("Products, ", response)
                setProducts(response);
            } catch (error) {
                console.error('Error al obtener los datos:', error);
            }
        };

        fetchData();
    }, []);

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    const handleValidate = (id) => {
        history.push(`/admin/validate-product/${id}`);
    };

    const handleDelete = (id) => {
        console.log('Eliminar producto:', id);
        // Lógica para eliminar producto
    };

    return (
        <Box sx={styles.mainBox}>
            <TopBar showSearchBar={true} showLogoutButton={true} />
            <Container sx={styles.mainContainer}>
                <Typography variant="h3" align="center" gutterBottom sx={{ color: '#629C44' }}>
                    Admin Panel
                </Typography>
                <Grid margin={'50px'}>
                    <TableContainer component={Paper}>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <TableCell>ID</TableCell>
                                    <TableCell>Nombre</TableCell>
                                    <TableCell>Estado</TableCell>
                                    <TableCell>Acciones</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {products.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((product) => (
                                    <TableRow key={product.id}>
                                        <TableCell>{product.id}</TableCell>
                                        <TableCell>{product.name}</TableCell>
                                        <TableCell>{product.state}</TableCell>
                                        <TableCell>
                                            <Button color="primary" onClick={() => handleValidate(product.id)}>Validar</Button>
                                            <Button color="secondary" onClick={() => handleDelete(product.id)}>Eliminar</Button>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                        <TablePagination
                            rowsPerPageOptions={[5, 10, 20]}
                            component="div"
                            count={products.length}
                            rowsPerPage={rowsPerPage}
                            page={page}
                            onPageChange={handleChangePage}
                            onRowsPerPageChange={handleChangeRowsPerPage}
                        />
                    </TableContainer>
                </Grid>
            </Container>
            <Footer />
        </Box>
    );
};

export default AdminPage;
