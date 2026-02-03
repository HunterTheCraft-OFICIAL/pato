// core/src/io/hunterthecraft/pato/data/TileType.java
package io.hunterthecraft.pato.data;

public enum TileType {
    // === TERRA: Biomas brasileiros ===
    AMAZONIA("debug_amazonia", "Amazônia", true),
    CERRADO("debug_cerrado", "Cerrado", true),
    CAATINGA("debug_caatinga", "Caatinga", true),
    AREIA_SUDESTE("debug_areia_sudeste", "Areia (SE)", true),

    // === ÁGUA: Sistema hídrico modular ===
    RIO_RETO_V("debug_rio_reto_V", "Rio Reto (V)", false),
    RIO_CURVA_NE("debug_curva_NE", "Curva NE", false),
    LAGO_G("debug_lago_G", "Lago (G)", false),
    FOZ_N("debug_foz_N", "Foz (N)", false),
    CRUZAMENTO_P("debug_cruzamento_P", "Cruzamento (P)", false),
    PONTA_S("debug_ponta_S", "Ponta Sul", false);

    public final String key;
    public final String name;
    public final boolean buildable;

    TileType(String key, String name, boolean buildable) {
        this.key = key;
        this.name = name;
        this.buildable = buildable;
    }

    public String getAssetPath() {
        if (isWater()) {
            return "tiles_hydric/" + key + ".png";
        }
        return "tiles/" + key + ".png";
    }

    public boolean isWater() {
        return this == RIO_RETO_V || this == RIO_CURVA_NE ||
               this == LAGO_G || this == FOZ_N ||
               this == CRUZAMENTO_P || this == PONTA_S;
    }
}