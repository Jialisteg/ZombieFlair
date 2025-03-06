import React from 'react';
import { Box, Typography, Grid, Paper, Tooltip, styled } from '@mui/material';

// Styled components for the visualization
const FloorContainer = styled(Box)(({ theme }) => ({
  marginBottom: theme.spacing(4),
  borderRadius: theme.shape.borderRadius,
  padding: theme.spacing(2),
  backgroundColor: theme.palette.grey[100]
}));

const RoomCard = styled(Paper)(({ 
  theme, 
  hasZombies, 
  isStaircase, 
  sensorAlert, 
  isHighlighted,
  hasPracticante
}) => ({
  height: '120px',
  width: '100%',
  padding: theme.spacing(2),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  position: 'relative',
  cursor: 'pointer',
  transition: 'all 0.3s ease',
  backgroundColor: isHighlighted 
    ? theme.palette.primary.light 
    : isStaircase 
      ? theme.palette.grey[300] 
      : theme.palette.background.paper,
  border: '1px solid',
  borderColor: isHighlighted 
    ? theme.palette.primary.main 
    : theme.palette.grey[300],
  boxShadow: isHighlighted 
    ? `0 0 10px ${theme.palette.primary.main}` 
    : theme.shadows[1],
  '&:hover': {
    transform: 'translateY(-5px)',
    boxShadow: theme.shadows[6]
  }
}));

const RoomIcon = styled('div')(({ theme }) => ({
  fontSize: '24px',
  margin: theme.spacing(1, 0),
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  minHeight: '30px'
}));

const StatusIndicator = styled('div')(({ theme, color }) => ({
  position: 'absolute',
  top: '8px',
  right: '8px',
  width: '12px',
  height: '12px',
  borderRadius: '50%',
  backgroundColor: color
}));

const PracticanteIndicator = styled('div')(({ theme }) => ({
  position: 'absolute',
  bottom: '8px',
  right: '8px',
  fontSize: '24px',
  fontWeight: 'bold',
  filter: 'drop-shadow(0px 0px 2px rgba(0,0,0,0.7))',
  zIndex: 10
}));

// Función para formatear el número de habitación según el nuevo formato
const formatRoomNumber = (floorIndex, roomNumber) => {
  // Sumamos 1 al índice del piso para que empiece en 1
  const floorNumber = floorIndex + 1;
  // Para las escaleras, mantenemos un formato especial
  if (roomNumber === 0) {
    return `E${floorNumber}`;
  }
  // Para habitaciones normales, usamos el formato piso + número secuencial
  return `${floorNumber}${roomNumber.toString().padStart(2, '0')}`;
};

const BuildingVisualization = ({ data, onRoomClick, selectedRoom }) => {
  if (!data || !data.building || !Array.isArray(data.building)) {
    return (
      <Box sx={{ textAlign: 'center', p: 3 }}>
        <Typography variant="body1">No hay datos del edificio disponibles.</Typography>
      </Box>
    );
  }

  // Reversing to display the highest floor at the top
  const floors = [...data.building].reverse();

  return (
    <Box sx={{ py: 2 }}>
      {floors.map((floor, floorIndex) => {
        // Calculamos el índice real del piso (considerando la inversión)
        const actualFloorIndex = data.building.length - 1 - floorIndex;
        // Sumamos 1 para que los pisos comiencen en 1 en lugar de 0
        const displayFloorNumber = actualFloorIndex + 1;
        
        return (
          <FloorContainer key={`floor-${actualFloorIndex}`}>
            <Typography variant="h6" gutterBottom>
              Piso {displayFloorNumber}
            </Typography>
            <Grid container spacing={2}>
              {floor.map((room) => {
                const isSelected = selectedRoom && 
                  selectedRoom.floor === room.floor && 
                  selectedRoom.room === room.room;
                
                const hasPracticante = data.practicante && 
                  data.practicante.floor === room.floor && 
                  data.practicante.room === room.room;
                
                // Formateamos el número de habitación según el nuevo formato
                const formattedRoomNumber = formatRoomNumber(room.floor, room.room);
                
                return (
                  <Grid 
                    item 
                    xs={6} 
                    sm={4} 
                    md={3} 
                    lg={2} 
                    key={`room-${room.floor}-${room.room}`}
                    onClick={() => onRoomClick(room.floor, room.room)}
                  >
                    <Tooltip 
                      title={`${room.is_staircase ? 'Escalera' : 'Habitación'} ${formattedRoomNumber}${room.has_zombies ? ' - ¡Zombie!' : ''}${!room.is_staircase && room.sensor_alert ? ' - ¡Alerta de Sensor!' : ''}${hasPracticante ? ' - ¡El practicante está aquí!' : ''}`} 
                      arrow
                    >
                      <RoomCard 
                        hasZombies={room.has_zombies} 
                        isStaircase={room.is_staircase}
                        sensorAlert={!room.is_staircase && room.sensor_alert}
                        isHighlighted={isSelected}
                        hasPracticante={hasPracticante}
                      >
                        <Typography variant="subtitle1">
                          {room.is_staircase ? `Escalera ${formattedRoomNumber}` : `Hab. ${formattedRoomNumber}`}
                        </Typography>
                        
                        <RoomIcon>
                          {room.is_staircase ? '🪜' : (
                            <>
                              {room.has_zombies && <span style={{ marginRight: '5px' }}>🧟</span>}
                              {hasPracticante && <span style={{ marginRight: '5px' }}>🧑‍🎓</span>}
                              <span>🚪</span>
                            </>
                          )}
                        </RoomIcon>
                        
                        {!room.is_staircase && (
                          <StatusIndicator color={room.sensor_alert ? '#ff5722' : '#4caf50'} />
                        )}
                      </RoomCard>
                    </Tooltip>
                  </Grid>
                );
              })}
            </Grid>
          </FloorContainer>
        );
      })}
    </Box>
  );
};

export default BuildingVisualization; 