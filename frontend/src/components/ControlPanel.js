import React from 'react';
import { 
  Grid, 
  Button, 
  ButtonGroup, 
  Typography, 
  Divider, 
  Stack,
  Switch,
  FormControlLabel,
  Chip
} from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import AddIcon from '@mui/icons-material/Add';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import CleaningServicesIcon from '@mui/icons-material/CleaningServices';
import NotificationsOffIcon from '@mui/icons-material/NotificationsOff';
import LocalFireDepartmentIcon from '@mui/icons-material/LocalFireDepartment';

// Función para formatear el número de habitación
const formatRoomNumber = (floorIndex, roomNumber) => {
  // Sumamos 1 al índice del piso para que empiece en 1
  const floorNumber = floorIndex + 1;
  // Para habitaciones normales, usamos el formato piso + número secuencial
  return `${floorNumber}${roomNumber.toString().padStart(2, '0')}`;
};

const ControlPanel = ({ 
  onAdvanceTurn,
  onAddZombie,
  onAddPracticante,
  onToggleZombieGeneration,
  onUseSecretWeapon,
  onToggleAutoRun,
  onCleanRoom,
  onResetSensor,
  selectedRoom,
  simulationState,
  autoRunning,
  loading
}) => {
  // Check if the game is over
  const isGameOver = simulationState && simulationState.game_over;
  
  // Check if we have a practicante already
  const hasPracticante = simulationState && simulationState.practicante !== null;
  
  // Formatear la habitación seleccionada si existe
  const formattedSelectedRoom = selectedRoom 
    ? formatRoomNumber(selectedRoom.floor, selectedRoom.room)
    : null;
  
  return (
    <Grid container spacing={3}>
      {/* Main simulation controls */}
      <Grid item xs={12} md={4}>
        <Typography variant="subtitle1" gutterBottom>
          Controles de Simulación
        </Typography>
        <Stack spacing={2}>
          <Button
            variant="contained"
            color="primary"
            startIcon={<PlayArrowIcon />}
            onClick={onAdvanceTurn}
            disabled={loading || isGameOver || !simulationState}
            fullWidth
          >
            Avanzar Turno
          </Button>
          <FormControlLabel
            control={
              <Switch
                checked={autoRunning}
                onChange={onToggleAutoRun}
                disabled={loading || isGameOver || !simulationState}
                color="primary"
              />
            }
            label={autoRunning ? "Ejecución automática activada" : "Ejecución automática desactivada"}
          />
          <Button
            variant="outlined"
            startIcon={autoRunning ? <StopIcon /> : <PlayArrowIcon />}
            onClick={onToggleAutoRun}
            disabled={loading || isGameOver || !simulationState}
            color={autoRunning ? "secondary" : "primary"}
            fullWidth
          >
            {autoRunning ? "Detener Ejecución Automática" : "Iniciar Ejecución Automática"}
          </Button>
          <FormControlLabel
            control={
              <Switch
                checked={simulationState?.zombie_generation_enabled || false}
                onChange={onToggleZombieGeneration}
                disabled={loading || isGameOver || !simulationState}
                color="primary"
              />
            }
            label={simulationState?.zombie_generation_enabled ? "Generación de zombies activada" : "Generación de zombies desactivada"}
          />
        </Stack>
      </Grid>
      
      {/* Character controls */}
      <Grid item xs={12} md={4}>
        <Typography variant="subtitle1" gutterBottom>
          Personajes
        </Typography>
        <Stack spacing={2}>
          <Button
            variant="contained"
            color="primary"
            startIcon={<AddIcon />}
            onClick={onAddZombie}
            disabled={loading || isGameOver || !simulationState}
            fullWidth
          >
            Agregar Zombie
          </Button>
          <Button
            variant="contained"
            color="primary"
            startIcon={<PersonAddIcon />}
            onClick={onAddPracticante}
            disabled={loading || isGameOver || !simulationState || hasPracticante}
            fullWidth
          >
            Agregar Practicante
          </Button>
          <Button
            variant="contained"
            color="secondary"
            startIcon={<LocalFireDepartmentIcon />}
            onClick={onUseSecretWeapon}
            disabled={loading || isGameOver || !simulationState}
            fullWidth
          >
            Activar Arma Secreta
          </Button>
        </Stack>
      </Grid>
      
      {/* Room controls */}
      <Grid item xs={12} md={4}>
        <Typography variant="subtitle1" gutterBottom>
          Acciones en Habitaciones
          {selectedRoom && (
            <Chip 
              label={`Seleccionada: Habitación ${formattedSelectedRoom}`} 
              color="primary" 
              size="small" 
              sx={{ ml: 1 }}
            />
          )}
        </Typography>
        <Stack spacing={2}>
          <Button
            variant="outlined"
            startIcon={<CleaningServicesIcon />}
            onClick={onCleanRoom}
            disabled={loading || isGameOver || !simulationState || !selectedRoom}
            fullWidth
          >
            Limpiar Habitación
          </Button>
          <Button
            variant="outlined"
            startIcon={<NotificationsOffIcon />}
            onClick={onResetSensor}
            disabled={loading || isGameOver || !simulationState || !selectedRoom}
            fullWidth
          >
            Restablecer Sensor
          </Button>
          {!selectedRoom && (
            <Typography variant="body2" color="text.secondary" align="center">
              Seleccione una habitación para realizar acciones
            </Typography>
          )}
        </Stack>
      </Grid>
      
      {/* Game over message */}
      {isGameOver && (
        <Grid item xs={12}>
          <Divider sx={{ my: 2 }} />
          <Typography variant="h6" color="error" align="center">
            FIN DEL JUEGO: {simulationState.game_over_reason === 'practicante_capturado' 
              ? '¡El practicante ha sido capturado por un zombie!' 
              : '¡Todas las habitaciones han sido infestadas con zombies!'}
          </Typography>
        </Grid>
      )}
    </Grid>
  );
};

export default ControlPanel; 