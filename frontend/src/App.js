import React, { useState, useEffect } from 'react';
import { 
  ThemeProvider, 
  createTheme, 
  CssBaseline, 
  Container, 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  Paper, 
  Grid,
  Button,
  CircularProgress,
  Alert,
  Snackbar
} from '@mui/material';
import BuildingVisualization from './components/BuildingVisualization';
import ControlPanel from './components/ControlPanel';
import StatsPanel from './components/StatsPanel';
import ConfigPanel from './components/ConfigPanel';
import { fetchSimulationState, setupBuilding, advanceSimulation, addZombie, addPracticante, cleanRoom, resetSensor, toggleZombieGeneration, triggerSecretWeapon, autoRun, resetSimulation } from './api/simulationApi';

// Create a theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#2e7d32', // Green
    },
    secondary: {
      main: '#d32f2f', // Red
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
});

function App() {
  const [simulationState, setSimulationState] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [autoRunning, setAutoRunning] = useState(false);
  const [notification, setNotification] = useState({ show: false, message: '', severity: 'info' });
  const [selectedRoom, setSelectedRoom] = useState(null);

  // Initial load
  useEffect(() => {
    loadSimulationState();
  }, []);

  // Auto refresh when auto-running
  useEffect(() => {
    let interval;
    if (autoRunning) {
      interval = setInterval(() => {
        loadSimulationState();
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRunning]);

  const loadSimulationState = async () => {
    try {
      setLoading(true);
      const data = await fetchSimulationState();
      setSimulationState(data);
      setError(null);
    } catch (err) {
      setError('Error al cargar el estado de la simulación');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSetupBuilding = async (config) => {
    try {
      setLoading(true);
      await setupBuilding(config);
      await loadSimulationState();
      showNotification('¡Edificio configurado correctamente!', 'success');
    } catch (err) {
      setError('Error al configurar el edificio');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAdvanceTurn = async () => {
    try {
      setLoading(true);
      const result = await advanceSimulation();
      await loadSimulationState();
      
      // Si se generó un nuevo zombie, mostramos notificación con el formato actualizado
      if (result.new_zombie_generated && result.new_zombie_location) {
        const [floor, room] = result.new_zombie_location;
        const formattedRoom = formatRoomNumber(floor, room);
        showNotification(`¡Se ha generado un nuevo zombie en la habitación ${formattedRoom}!`, 'warning');
      }
      
      if (result.game_over) {
        let message = '¡Juego terminado! ';
        if (result.game_over_reason === 'practicante_capturado') {
          message += '¡El practicante ha sido capturado por un zombie!';
        } else {
          message += '¡Todas las habitaciones han sido infestadas con zombies!';
        }
        showNotification(message, 'error');
      }
    } catch (err) {
      setError('Error al avanzar turno');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Función para formatear el número de habitación
  const formatRoomNumber = (floorIndex, roomNumber) => {
    // Sumamos 1 al índice del piso para que empiece en 1
    const floorNumber = floorIndex + 1;
    // Para habitaciones normales, usamos el formato piso + número secuencial
    return `${floorNumber}${roomNumber.toString().padStart(2, '0')}`;
  };

  const handleAddZombie = async () => {
    try {
      const result = await addZombie();
      await loadSimulationState();
      
      if (result.added) {
        const formattedRoom = formatRoomNumber(result.floor, result.room);
        showNotification(`¡Se ha agregado un nuevo zombie en la habitación ${formattedRoom}!`, 'warning');
      } else {
        showNotification('No se pudo agregar un zombie (todas las habitaciones podrían estar infestadas).', 'info');
      }
    } catch (err) {
      setError('Error al agregar zombie');
      console.error(err);
    }
  };

  const handleAddPracticante = async () => {
    try {
      const result = await addPracticante();
      await loadSimulationState();
      
      if (!result.error) {
        const formattedRoom = formatRoomNumber(result.floor, result.room);
        showNotification(`¡Se ha añadido un practicante en la habitación ${formattedRoom}!`, 'success');
      } else {
        showNotification(result.error, 'info');
      }
    } catch (err) {
      setError('Error al agregar practicante');
      console.error(err);
    }
  };

  const handleCleanRoom = async (floor, room) => {
    try {
      const result = await cleanRoom(floor, room);
      await loadSimulationState();
      
      if (result.cleaned) {
        const formattedRoom = formatRoomNumber(floor, room);
        showNotification(`¡La habitación ${formattedRoom} ha sido limpiada!`, 'success');
      } else {
        showNotification(result.message || 'No se pudo limpiar la habitación.', 'info');
      }
    } catch (err) {
      setError('Error al limpiar habitación');
      console.error(err);
    }
  };

  const handleResetSensor = async (floor, room) => {
    try {
      const result = await resetSensor(floor, room);
      await loadSimulationState();
      
      if (result.reset) {
        const formattedRoom = formatRoomNumber(floor, room);
        showNotification(`¡Sensor en la habitación ${formattedRoom} restablecido!`, 'success');
      } else {
        showNotification(result.message || 'No se pudo restablecer el sensor.', 'info');
      }
    } catch (err) {
      setError('Error al restablecer sensor');
      console.error(err);
    }
  };

  const handleToggleZombieGeneration = async () => {
    try {
      const result = await toggleZombieGeneration();
      await loadSimulationState();
      
      const status = result.zombie_generation_enabled ? 'activada' : 'desactivada';
      showNotification(`¡Generación de zombies ${status}!`, 'info');
    } catch (err) {
      setError('Error al cambiar generación de zombies');
      console.error(err);
    }
  };

  const handleUseSecretWeapon = async () => {
    try {
      // Redirección al enlace específico cuando se usa el arma secreta
      window.open('https://youtu.be/dQw4w9WgXcQ?si=L6gTOSJZpsrg8jLS', '_blank');
      
      // Opcionalmente, podemos seguir mostrando una notificación
      showNotification('¡Activando arma secreta! Abriendo portal externo...', 'success');
      
      // No llamamos a la API original
      // const result = await triggerSecretWeapon();
      // await loadSimulationState();
      // showNotification(`¡El arma secreta ha limpiado ${result.cleaned_count} habitaciones!`, 'success');
    } catch (err) {
      setError('Error al usar el arma secreta');
      console.error(err);
    }
  };

  const handleToggleAutoRun = async () => {
    try {
      const newAutoRunState = !autoRunning;
      await autoRun(newAutoRunState);
      setAutoRunning(newAutoRunState);
      
      showNotification(`Ejecución automática ${newAutoRunState ? 'activada' : 'desactivada'}`, 'info');
    } catch (err) {
      setError('Error al cambiar modo automático');
      console.error(err);
    }
  };

  const handleRoomClick = (floor, room) => {
    setSelectedRoom({ floor, room });
  };

  const handleActionOnSelectedRoom = (action) => {
    if (!selectedRoom) return;
    
    const { floor, room } = selectedRoom;
    if (action === 'clean') {
      handleCleanRoom(floor, room);
    } else if (action === 'reset') {
      handleResetSensor(floor, room);
    }
  };

  const handleResetSimulation = async () => {
    try {
      await resetSimulation();
      setAutoRunning(false);
      await loadSimulationState();
      showNotification('¡La simulación ha sido reiniciada!', 'success');
    } catch (err) {
      setError('Error al reiniciar la simulación');
      console.error(err);
    }
  };

  const showNotification = (message, severity = 'info') => {
    setNotification({
      show: true,
      message,
      severity
    });
  };

  const closeNotification = () => {
    setNotification(prev => ({ ...prev, show: false }));
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Simulación de Edificio con Zombies
            </Typography>
            <Button 
              color="inherit" 
              onClick={handleResetSimulation}
            >
              Reiniciar Simulación
            </Button>
          </Toolbar>
        </AppBar>

        <Container maxWidth="xl" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <Grid container spacing={3}>
            {/* Configuration Panel - Left Side */}
            <Grid item xs={12} md={4}>
              <Paper sx={{ p: 2, height: '100%' }}>
                <Typography variant="h6" gutterBottom>
                  Configuración
                </Typography>
                <ConfigPanel 
                  onSetupBuilding={handleSetupBuilding} 
                  loading={loading}
                  simulationExists={!!simulationState}
                />
              </Paper>
            </Grid>

            {/* Building Visualization - Right Side */}
            <Grid item xs={12} md={8}>
              <Paper sx={{ p: 2, minHeight: '400px' }}>
                <Typography variant="h6" gutterBottom>
                  Visualización del Edificio
                </Typography>
                {loading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                    <CircularProgress />
                  </Box>
                ) : simulationState ? (
                  <BuildingVisualization 
                    data={simulationState} 
                    onRoomClick={handleRoomClick}
                    selectedRoom={selectedRoom}
                  />
                ) : (
                  <Box sx={{ p: 2, textAlign: 'center' }}>
                    <Typography>No hay edificio configurado. Por favor, configure un edificio primero.</Typography>
                  </Box>
                )}
              </Paper>
            </Grid>

            {/* Control Panel */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Controles
                </Typography>
                <ControlPanel 
                  onAdvanceTurn={handleAdvanceTurn}
                  onAddZombie={handleAddZombie}
                  onAddPracticante={handleAddPracticante}
                  onToggleZombieGeneration={handleToggleZombieGeneration}
                  onUseSecretWeapon={handleUseSecretWeapon}
                  onToggleAutoRun={handleToggleAutoRun}
                  onCleanRoom={() => handleActionOnSelectedRoom('clean')}
                  onResetSensor={() => handleActionOnSelectedRoom('reset')}
                  selectedRoom={selectedRoom}
                  simulationState={simulationState}
                  autoRunning={autoRunning}
                  loading={loading}
                />
              </Paper>
            </Grid>
            
            {/* Stats Panel - Full Width at Bottom */}
            <Grid item xs={12}>
              <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Estadísticas
                </Typography>
                {simulationState ? (
                  <StatsPanel data={simulationState} />
                ) : (
                  <Box sx={{ p: 2, textAlign: 'center' }}>
                    <Typography>No hay datos de simulación disponibles. Por favor, configure un edificio.</Typography>
                  </Box>
                )}
              </Paper>
            </Grid>
          </Grid>
        </Container>

        <Snackbar 
          open={notification.show} 
          autoHideDuration={6000} 
          onClose={closeNotification}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert onClose={closeNotification} severity={notification.severity}>
            {notification.message}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  );
}

export default App; 