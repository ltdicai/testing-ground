import java.util.Objects; // Used for potential null checks, though not strictly needed in this direct translation

// --- Radio Class ---
class Radio {
    private String marca;
    private int potencia; // Assuming potencia is an integer
    private Vehiculo vehiculo; // Reference back to the vehicle it's in

    // Constructor
    public Radio(String marca, int potencia, Vehiculo vehiculo) {
        this.marca = marca;
        this.potencia = potencia;
        this.vehiculo = vehiculo; // Initially connected to the vehicle creating it
    }

    // Checks if the radio is currently associated with a vehicle
    public boolean estaConectada() {
        return this.vehiculo != null;
    }

    // Package-private: Intended for use mainly by Vehiculo/AutoNuevo
    // Disconnects this radio from its current vehicle
    void desconectarVehiculo() {
        this.vehiculo = null;
    }

    // Package-private: Intended for use mainly by Vehiculo/AutoNuevo
    // Connects this radio to a specific vehicle
    void conectarVehiculo(Vehiculo vehiculo) {
        this.vehiculo = vehiculo;
    }

    // Getters (optional, but good practice)
    public String getMarca() {
        return marca;
    }

    public int getPotencia() {
        return potencia;
    }

    public Vehiculo getVehiculo() {
        return vehiculo;
    }


    @Override
    public String toString() {
        String vehiculoMarca = (this.vehiculo != null) ? this.vehiculo.getMarca() : "ninguno";
        return String.format("%s (marca: %s, potencia: %d, vehiculo: %s)",
                             this.getClass().getSimpleName(),
                             this.marca,
                             this.potencia,
                             vehiculoMarca);
    }
}

// --- Vehiculo Abstract Class ---
abstract class Vehiculo {
    private String marca;
    private String modelo;
    // Protected so subclasses like AutoNuevo can directly access/modify it
    protected Radio radio;

    // Constructor
    public Vehiculo(String marca, String modelo, String marcaRadio, int potenciaRadio) {
        this.marca = marca;
        this.modelo = modelo;
        // Create and connect the initial radio upon vehicle creation
        this.radio = new Radio(marcaRadio, potenciaRadio, this);
    }

    // Getters
    public String getMarca() {
        return marca;
    }

    public String getModelo() {
        return modelo;
    }

    public Radio getRadio() {
        return radio;
    }


    @Override
    public String toString() {
        return String.format("%s (marca: %s, modelo: %s, radio: %s)",
                             this.getClass().getSimpleName(),
                             this.marca,
                             this.modelo,
                             this.radio != null ? this.radio.toString() : "ninguna");
    }

    // --- Methods related to radio management might go here if common ---
    // --- but in the Python example, they are specific to AutoNuevo ---

}

// --- AutoNuevo Class ---
class AutoNuevo extends Vehiculo {

    // Constructor
    public AutoNuevo(String marca, String modelo, String marcaRadio, int potenciaRadio) {
        super(marca, modelo, marcaRadio, potenciaRadio); // Call parent constructor
    }

    /**
     * Assigns a new radio to this vehicle.
     * If the vehicle already has a radio, it's disconnected first.
     * The new radio must not be connected to another vehicle already.
     * @param nuevoRadio The new Radio object to assign.
     */
    public void asignarRadio(Radio nuevoRadio) {
        Objects.requireNonNull(nuevoRadio, "Cannot assign a null radio."); // Added null check

        if (!nuevoRadio.estaConectada()) {
            // If this vehicle currently has a radio, disconnect it first
            if (this.radio != null) {
                this.desconectarRadioActual();
            }
            // Connect the new radio to this vehicle
            this.conectarNuevaRadio(nuevoRadio);
        } else {
            System.out.println("Error: La radio ya está conectada a otro vehículo.");
            // Optionally throw an exception instead of printing
            // throw new IllegalStateException("La radio ya está conectada a otro vehículo.");
        }
    }

    /**
     * Private helper method to disconnect the current radio.
     * Tells the radio it's no longer connected and removes the reference from the vehicle.
     */
    private void desconectarRadioActual() {
        if (this.radio != null) {
            this.radio.desconectarVehiculo(); // Tell the radio it's disconnected
            this.radio = null; // Remove reference from vehicle
        }
    }

    /**
     * Private helper method to connect a new radio.
     * Tells the new radio it's connected to this vehicle and sets the vehicle's reference.
     * @param nuevaRadio The new radio to connect.
     */
    private void conectarNuevaRadio(Radio nuevaRadio) {
        nuevaRadio.conectarVehiculo(this); // Tell the radio it's connected to us
        this.radio = nuevaRadio; // Set our radio reference
    }

    // toString is inherited from Vehiculo
}

// --- Example Usage (Optional Main Class) ---
class Main {
    public static void main(String[] args) {
        // Create a new car, which automatically gets an initial radio
        AutoNuevo miAuto = new AutoNuevo("Toyota", "Corolla", "Pioneer", 50);
        System.out.println("Auto inicial: " + miAuto);
        System.out.println("Radio inicial: " + miAuto.getRadio());
        System.out.println("¿Radio inicial conectada? " + miAuto.getRadio().estaConectada());
        System.out.println("---");

        // Create a separate radio, initially not connected to anything implicitly
        // (We need a vehicle reference for the constructor, maybe pass null or rethink Radio constructor if needed standalone)
        // Let's create another car to demonstrate swapping
        AutoNuevo otroAuto = new AutoNuevo("Ford", "Fiesta", "Sony", 45);
        System.out.println("Otro Auto: " + otroAuto);
        Radio radioSony = otroAuto.getRadio(); // Get the radio from the second car
        System.out.println("---");

        // Try to assign the Sony radio (already in otroAuto) to miAuto (should fail)
        System.out.println("Intentando asignar radio Sony (de otroAuto) a miAuto:");
        try {
            miAuto.asignarRadio(radioSony);
        } catch (Exception e) {
            System.out.println("Capturada Excepción: " + e.getMessage());
        }
        System.out.println("Estado miAuto: " + miAuto);
        System.out.println("Estado otroAuto: " + otroAuto);
        System.out.println("---");


        // Create a truly new, unassigned radio (this requires adjusting the Radio constructor or logic)
        // For this example, let's simulate getting a new radio instance by creating one not tied to a car initially
        // Note: The current Radio constructor REQUIRES a vehicle. Let's make a new one for the example.
        Radio radioNueva = new Radio("Kenwood", 60, null); // Explicitly start unattached
        System.out.println("Nueva Radio (Kenwood): " + radioNueva);
        System.out.println("¿Nueva Radio conectada? " + radioNueva.estaConectada());
        System.out.println("---");

        // Assign the new Kenwood radio to miAuto
        System.out.println("Asignando radio Kenwood a miAuto:");
        Radio radioPioneerOriginal = miAuto.getRadio(); // Keep track of the old one
        miAuto.asignarRadio(radioNueva);

        System.out.println("Estado miAuto: " + miAuto);
        System.out.println("Estado radio Kenwood: " + radioNueva);
        System.out.println("Estado radio Pioneer (original): " + radioPioneerOriginal); // Should now be disconnected
        System.out.println("¿Radio Pioneer conectada? " + radioPioneerOriginal.estaConectada());

    }
}