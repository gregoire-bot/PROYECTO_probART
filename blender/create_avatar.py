import bpy
import os
import sys
from mathutils import Vector


# ============================================================
# CONFIGURACIÓN POR DEFECTO
# ============================================================

GENERO = "male"
EDAD = "young"
ALTURA = "average"
PESO = "averageweight"
MUSCULO = "averagemuscle"
PROPORCIONES = "average"


# ============================================================
# APARIENCIA
# ============================================================

PIEL = "#D9A27F"

# Identificador de textura de ojos MPFB
OJOS = "brown"

# Identificador del modelo de cabello MPFB
CABELLO = "short01"

# Color independiente del modelo de cabello
COLOR_CABELLO = "#3A2418"


# ============================================================
# OPCIONES DE CABELLO
# ============================================================

CABELLOS_DISPONIBLES = {
    "short01": "Corto 01",
    "short02": "Corto 02",
    "short03": "Corto 03",
    "short04": "Corto 04",
    "bob01": "Bob 01",
    "bob02": "Bob 02",
    "long01": "Largo 01",
    "ponytail01": "Cola de caballo",
    "braid01": "Trenzado",
    "afro01": "Afro",
}


# ============================================================
# OPCIONES DE OJOS
# ============================================================

OJOS_DISPONIBLES = {
    "brown": "Marrón",
    "brownlight": "Marrón claro",
    "blue": "Azul",
    "bluegreen": "Azul verdoso",
    "deepblue": "Azul profundo",
    "green": "Verde",
    "grey": "Gris",
    "ice": "Hielo",
    "lightblue": "Azul claro",
}


# ============================================================
# RUTAS DE MPFB
# ============================================================

MPFB_DATA = "/home/felix/felix/MPFB/data"

HAIR_DIR = os.path.join(
    MPFB_DATA,
    "hair"
)

EYES_DIR = os.path.join(
    MPFB_DATA,
    "eyes"
)

EYES_MATERIAL_DIR = os.path.join(
    EYES_DIR,
    "materials"
)


# ============================================================
# EXPORTACIÓN
# ============================================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "models",
    "avatars"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "avatar.glb"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# ARGUMENTOS
# ============================================================

def argumentos():

    global GENERO
    global EDAD
    global ALTURA
    global PESO
    global MUSCULO
    global PROPORCIONES
    global PIEL
    global OJOS
    global CABELLO
    global COLOR_CABELLO

    args = (
        sys.argv[sys.argv.index("--") + 1:]
        if "--" in sys.argv
        else []
    )

    valores = {}

    i = 0

    while i < len(args):

        if (
            args[i].startswith("--")
            and i + 1 < len(args)
        ):

            valores[args[i][2:]] = args[i + 1]

            i += 2

        else:

            i += 1

    GENERO = valores.get(
        "genero",
        GENERO
    )

    EDAD = valores.get(
        "edad",
        EDAD
    )

    ALTURA = valores.get(
        "altura",
        ALTURA
    )

    PESO = valores.get(
        "peso",
        PESO
    )

    MUSCULO = valores.get(
        "musculo",
        MUSCULO
    )

    PROPORCIONES = valores.get(
        "proporciones",
        PROPORCIONES
    )

    PIEL = valores.get(
        "piel",
        PIEL
    )

    OJOS = valores.get(
        "ojos",
        OJOS
    )

    CABELLO = valores.get(
        "cabello",
        CABELLO
    )

    COLOR_CABELLO = valores.get(
        "colorCabello",
        COLOR_CABELLO
    )


# ============================================================
# VALIDACIÓN DE OPCIONES
# ============================================================

def validar_opciones():

    global CABELLO
    global COLOR_CABELLO
    global OJOS

    # --------------------------------------------------------
    # CABELLO
    # --------------------------------------------------------

    if CABELLO not in CABELLOS_DISPONIBLES:

        print(
            "AVISO: cabello no disponible:",
            CABELLO
        )

        print(
            "Se utilizará: short01"
        )

        CABELLO = "short01"

    # --------------------------------------------------------
    # OJOS
    # --------------------------------------------------------

    if OJOS not in OJOS_DISPONIBLES:

        print(
            "AVISO: color de ojos no disponible:",
            OJOS
        )

        print(
            "Se utilizará: brown"
        )

        OJOS = "brown"

    # --------------------------------------------------------
    # COLOR DE CABELLO
    # --------------------------------------------------------

    try:

        hex_rgba(
            COLOR_CABELLO
        )

    except Exception as error:

        print(
            "AVISO: color de cabello inválido:",
            COLOR_CABELLO
        )

        print(
            "Detalle:",
            error
        )

        print(
            "Se utilizará: #3A2418"
        )

        COLOR_CABELLO = "#3A2418"

    print(
        "================================"
    )

    print(
        "OPCIONES SELECCIONADAS"
    )

    print(
        "Cabello:",
        CABELLO,
        "-",
        CABELLOS_DISPONIBLES[CABELLO]
    )

    print(
        "Color cabello:",
        COLOR_CABELLO
    )

    print(
        "Ojos:",
        OJOS,
        "-",
        OJOS_DISPONIBLES[OJOS]
    )

    print(
        "================================"
    )


# ============================================================
# COLORES
# ============================================================

def hex_rgba(
    value,
    alpha=1.0
):

    """
    Convierte #RRGGBB a RGBA.
    """

    value = (
        value
        .strip()
        .lstrip("#")
    )

    if len(value) != 6:

        raise ValueError(
            f"Color inválido: #{value}. "
            "Use #RRGGBB"
        )

    return (
        int(value[0:2], 16) / 255.0,
        int(value[2:4], 16) / 255.0,
        int(value[4:6], 16) / 255.0,
        alpha,
    )


# ============================================================
# MATERIAL POR NOMBRE
# ============================================================

def material_por_nombre(nombre):

    return bpy.data.materials.get(
        nombre
    )


# ============================================================
# TINTAR MATERIAL
# ============================================================

def tintar_material(
    material,
    color_hex
):

    """
    Aplica el color manteniendo
    la textura original.

    Utiliza Multiply para conservar
    detalles y textura del material.
    """

    if (
        not material
        or not material.use_nodes
    ):

        return False

    try:

        color = hex_rgba(
            color_hex
        )

    except ValueError as error:

        print(
            "AVISO:",
            error
        )

        return False

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    bsdf = next(
        (
            n
            for n in nodes
            if n.type == "BSDF_PRINCIPLED"
        ),
        None
    )

    if not bsdf:

        print(
            "AVISO: No existe Principled BSDF en:",
            material.name
        )

        return False

    base = bsdf.inputs.get(
        "Base Color"
    )

    if not base:

        print(
            "AVISO: No existe Base Color en:",
            material.name
        )

        return False

    # --------------------------------------------------------
    # Buscar tintado existente
    # --------------------------------------------------------

    tint = nodes.get(
        "VirtualFit Tint"
    )

    if (
        tint
        and tint.type == "MIX_RGB"
    ):

        tint.inputs[2].default_value = color

        print(
            "Tint existente actualizado:",
            material.name
        )

        return True

    # --------------------------------------------------------
    # Guardar conexión anterior
    # --------------------------------------------------------

    old_link = (
        base.links[0]
        if base.links
        else None
    )

    # --------------------------------------------------------
    # Crear nodo de tintado
    # --------------------------------------------------------

    tint = nodes.new(
        "ShaderNodeMixRGB"
    )

    tint.name = (
        "VirtualFit Tint"
    )

    tint.label = (
        "VirtualFit Tint"
    )

    tint.blend_type = (
        "MULTIPLY"
    )

    # Factor máximo
    tint.inputs[0].default_value = 1.0

    # Color elegido
    tint.inputs[2].default_value = color

    # --------------------------------------------------------
    # Conectar textura original
    # --------------------------------------------------------

    if old_link:

        source_socket = (
            old_link.from_socket
        )

        links.remove(
            old_link
        )

        links.new(
            source_socket,
            tint.inputs[1]
        )

    else:

        tint.inputs[1].default_value = (
            base.default_value
        )

    # --------------------------------------------------------
    # Conectar tintado al BSDF
    # --------------------------------------------------------

    links.new(
        tint.outputs[0],
        base
    )

    print(
        "Material tintado:",
        material.name,
        "->",
        color_hex
    )

    return True


# ============================================================
# MATERIAL DE PIEL
# ============================================================

def preparar_material_piel():

    avatar = bpy.data.objects.get(
        "Human"
    )

    if not avatar:

        print(
            "ERROR: No existe el objeto Human"
        )

        return False

    textura = os.path.join(
        MPFB_DATA,
        "skins",
        "young_caucasian_male",
        "young_lightskinned_male_diffuse.png"
    )

    if not os.path.exists(
        textura
    ):

        print(
            "ERROR: No existe textura:",
            textura
        )

        return False

    imagen = bpy.data.images.get(
        "VirtualFit_Skin"
    )

    if not imagen:

        imagen = bpy.data.images.load(
            textura,
            check_existing=True
        )

        imagen.name = (
            "VirtualFit_Skin"
        )

    material = bpy.data.materials.get(
        "VirtualFit_Skin_Material"
    )

    if not material:

        material = bpy.data.materials.new(
            "VirtualFit_Skin_Material"
        )

    material.use_nodes = True

    nodes = (
        material.node_tree.nodes
    )

    links = (
        material.node_tree.links
    )

    nodes.clear()

    output = nodes.new(
        "ShaderNodeOutputMaterial"
    )

    bsdf = nodes.new(
        "ShaderNodeBsdfPrincipled"
    )

    tex = nodes.new(
        "ShaderNodeTexImage"
    )

    output.location = (
        400,
        0
    )

    bsdf.location = (
        100,
        0
    )

    tex.location = (
        -300,
        0
    )

    tex.image = imagen

    tex.image.colorspace_settings.name = (
        "sRGB"
    )

    links.new(
        tex.outputs["Color"],
        bsdf.inputs["Base Color"]
    )

    links.new(
        bsdf.outputs["BSDF"],
        output.inputs["Surface"]
    )

    avatar.data.materials.clear()

    avatar.data.materials.append(
        material
    )

    print(
        "MATERIAL DE PIEL CREADO:",
        material.name
    )

    print(
        "TEXTURA:",
        imagen.filepath
    )

    return True


# ============================================================
# APLICAR APARIENCIA DE PIEL
# ============================================================

def aplicar_apariencia():

    resultado = tintar_material(
        material_por_nombre(
            "VirtualFit_Skin_Material"
        ),
        PIEL
    )

    print(
        "Apariencia aplicada:",
        {
            "piel": resultado
        }
    )

    print(
        "Piel:",
        PIEL
    )

    return {
        "piel": resultado
    }


# ============================================================
# CONFIGURAR OPCIONES ASSET LIBRARY
# ============================================================

def configurar_asset_library():

    """
    Configuración comprobada en la instalación actual
    de MPFB.

    Evita que load_clothes() intente configurar
    un rig que no necesitamos para estos assets.
    """

    scene = bpy.context.scene

    try:

        scene.MPFB_ASLS_set_up_rigging = False

    except Exception as error:

        print(
            "AVISO configurando set_up_rigging:",
            error
        )

    try:

        scene.MPFB_ASLS_interpolate_weights = False

    except Exception as error:

        print(
            "AVISO configurando interpolate_weights:",
            error
        )

    try:

        scene.MPFB_ASLS_import_subrig = False

    except Exception as error:

        print(
            "AVISO configurando import_subrig:",
            error
        )

    try:

        scene.MPFB_ASLS_import_weights = False

    except Exception as error:

        print(
            "AVISO configurando import_weights:",
            error
        )

    print(
        "CONFIGURACIÓN MPFB ASLS:"
    )

    print(
        "set_up_rigging:",
        getattr(
            scene,
            "MPFB_ASLS_set_up_rigging",
            None
        )
    )

    print(
        "interpolate_weights:",
        getattr(
            scene,
            "MPFB_ASLS_interpolate_weights",
            None
        )
    )

    print(
        "import_subrig:",
        getattr(
            scene,
            "MPFB_ASLS_import_subrig",
            None
        )
    )

    print(
        "import_weights:",
        getattr(
            scene,
            "MPFB_ASLS_import_weights",
            None
        )
    )


# ============================================================
# SELECCIONAR HUMAN
# ============================================================

def activar_human():

    avatar = bpy.data.objects.get(
        "Human"
    )

    if not avatar:

        print(
            "ERROR: No existe Human."
        )

        return None

    bpy.ops.object.select_all(
        action="DESELECT"
    )

    avatar.select_set(
        True
    )

    bpy.context.view_layer.objects.active = (
        avatar
    )

    return avatar


# ============================================================
# OBTENER ARCHIVO DE CABELLO
# ============================================================

def obtener_archivo_cabello():

    carpeta = os.path.join(
        HAIR_DIR,
        CABELLO
    )

    archivo = os.path.join(
        carpeta,
        f"{CABELLO}.mhclo"
    )

    if not os.path.exists(
        archivo
    ):

        print(
            "ERROR: No existe el cabello:",
            archivo
        )

        return None

    return archivo


# ============================================================
# OBTENER TEXTURA DE OJOS
# ============================================================

def obtener_textura_ojos():

    archivo = os.path.join(
        EYES_MATERIAL_DIR,
        f"{OJOS}_eye.png"
    )

    if not os.path.exists(
        archivo
    ):

        print(
            "ERROR: No existe textura de ojos:",
            archivo
        )

        return None

    return archivo


# ============================================================
# OBTENER GEOMETRÍA DE OJOS
# ============================================================

def obtener_archivo_ojos():

    archivo = os.path.join(
        EYES_DIR,
        "high-poly",
        "high-poly.mhclo"
    )

    if not os.path.exists(
        archivo
    ):

        print(
            "ERROR: No existe:",
            archivo
        )

        return None

    return archivo


# ============================================================
# CREAR CABELLO
# ============================================================

def preparar_cabello():

    avatar = activar_human()

    if not avatar:

        return False

    archivo = obtener_archivo_cabello()

    if not archivo:

        return False

    print(
        "================================"
    )

    print(
        "CREANDO CABELLO MPFB"
    )

    print(
        "================================"
    )

    print(
        "Tipo:",
        CABELLO
    )

    print(
        "Nombre:",
        CABELLOS_DISPONIBLES[CABELLO]
    )

    print(
        "Color:",
        COLOR_CABELLO
    )

    print(
        "Archivo:",
        archivo
    )

    try:

        configurar_asset_library()

        resultado = bpy.ops.mpfb.load_clothes(
            filepath=archivo
        )

        print(
            "RESULTADO LOAD_CLOTHES CABELLO:",
            resultado
        )

        if "FINISHED" not in resultado:

            print(
                "ERROR: MPFB no pudo cargar "
                "el cabello."
            )

            return False

        # ----------------------------------------------------
        # Buscar objeto generado
        # ----------------------------------------------------

        cabello = bpy.data.objects.get(
            f"Human.{CABELLO}"
        )

        if not cabello:

            candidatos = [
                obj
                for obj in bpy.context.scene.objects
                if obj.name.startswith("Human.")
                and obj != avatar
            ]

            if candidatos:

                cabello = candidatos[-1]

        if cabello:

            print(
                "CABELLO CREADO:",
                cabello.name
            )

            # ------------------------------------------------
            # Aplicar color
            # ------------------------------------------------

            color_ok = aplicar_color_cabello(
                cabello
            )

            if color_ok:

                print(
                    "COLOR DE CABELLO APLICADO CORRECTAMENTE"
                )

            else:

                print(
                    "AVISO: El cabello fue creado, "
                    "pero no se pudo aplicar el color."
                )

            return cabello

        print(
            "AVISO: El cabello fue cargado, "
            "pero no se encontró automáticamente "
            "el objeto generado."
        )

        return False

    except Exception as error:

        print(
            "ERROR APLICANDO CABELLO:",
            error
        )

        return False


# ============================================================
# APLICAR COLOR AL CABELLO
# ============================================================

def aplicar_color_cabello(objeto):

    if not objeto:

        print(
            "ERROR: No existe objeto de cabello."
        )

        return False

    print(
        "================================"
    )

    print(
        "APLICANDO COLOR DE CABELLO"
    )

    print(
        "Objeto:",
        objeto.name
    )

    print(
        "Color:",
        COLOR_CABELLO
    )

    try:

        materiales = []

        # ----------------------------------------------------
        # Material activo
        # ----------------------------------------------------

        if objeto.active_material:

            materiales.append(
                objeto.active_material
            )

        # ----------------------------------------------------
        # Todos los materiales
        # ----------------------------------------------------

        if hasattr(
            objeto.data,
            "materials"
        ):

            for material in objeto.data.materials:

                if (
                    material
                    and material not in materiales
                ):

                    materiales.append(
                        material
                    )

        # ----------------------------------------------------
        # Buscar materiales en hijos
        # ----------------------------------------------------

        for hijo in objeto.children:

            if hasattr(
                hijo.data,
                "materials"
            ):

                for material in hijo.data.materials:

                    if (
                        material
                        and material not in materiales
                    ):

                        materiales.append(
                            material
                        )

        if not materiales:

            print(
                "ERROR: El cabello no tiene materiales."
            )

            return False

        resultado = False

        # ----------------------------------------------------
        # Aplicar color
        # ----------------------------------------------------

        for material in materiales:

            print(
                "Material cabello:",
                material.name
            )

            aplicado = tintar_material(
                material,
                COLOR_CABELLO
            )

            if aplicado:

                resultado = True

                print(
                    "Color aplicado a:",
                    material.name
                )

        print(
            "================================"
        )

        if resultado:

            print(
                "COLOR DE CABELLO APLICADO:",
                COLOR_CABELLO
            )

        else:

            print(
                "AVISO: No se pudo tintar "
                "el material del cabello."
            )

        return resultado

    except Exception as error:

        print(
            "ERROR APLICANDO COLOR DE CABELLO:",
            error
        )

        return False


# ============================================================
# APLICAR TEXTURA DE OJOS
# ============================================================

def aplicar_textura_ojos(objeto):

    if not objeto:

        print(
            "ERROR: No existe objeto de ojos."
        )

        return False

    archivo = obtener_textura_ojos()

    if not archivo:

        return False

    try:

        material = objeto.active_material

        if not material:

            # Buscar primer material disponible
            if (
                hasattr(
                    objeto.data,
                    "materials"
                )
                and len(
                    objeto.data.materials
                ) > 0
            ):

                material = (
                    objeto.data.materials[0]
                )

        if not material:

            print(
                "ERROR: Los ojos no tienen "
                "material activo."
            )

            return False

        if not material.use_nodes:

            material.use_nodes = True

        nodes = material.node_tree.nodes

        # ----------------------------------------------------
        # Buscar diffuseTexture
        # ----------------------------------------------------

        nodo_textura = nodes.get(
            "diffuseTexture"
        )

        # ----------------------------------------------------
        # Si no existe, buscar cualquier Image Texture
        # ----------------------------------------------------

        if not nodo_textura:

            candidatos = [
                node
                for node in nodes
                if node.type == "TEX_IMAGE"
            ]

            if candidatos:

                nodo_textura = candidatos[0]

        if not nodo_textura:

            print(
                "ERROR: No se encontró nodo "
                "de textura en el material:",
                material.name
            )

            print(
                "NODOS DISPONIBLES:",
                [
                    node.name
                    for node in nodes
                ]
            )

            return False

        imagen = bpy.data.images.load(
            archivo,
            check_existing=True
        )

        nodo_textura.image = imagen

        print(
            "TEXTURA DE OJOS APLICADA:"
        )

        print(
            "Color:",
            OJOS
        )

        print(
            "Archivo:",
            archivo
        )

        print(
            "Material:",
            material.name
        )

        print(
            "Nodo:",
            nodo_textura.name
        )

        return True

    except Exception as error:

        print(
            "ERROR APLICANDO TEXTURA DE OJOS:",
            error
        )

        return False


# ============================================================
# CREAR OJOS
# ============================================================

def preparar_ojos():

    avatar = activar_human()

    if not avatar:

        return False

    ojos_file = obtener_archivo_ojos()

    if not ojos_file:

        return False

    textura_ojos = obtener_textura_ojos()

    if not textura_ojos:

        return False

    print(
        "================================"
    )

    print(
        "CREANDO OJOS MPFB"
    )

    print(
        "================================"
    )

    print(
        "Color:",
        OJOS
    )

    print(
        "Nombre:",
        OJOS_DISPONIBLES[OJOS]
    )

    print(
        "MHCLO:",
        ojos_file
    )

    print(
        "TEXTURA:",
        textura_ojos
    )

    try:

        configurar_asset_library()

        resultado = bpy.ops.mpfb.load_clothes(
            filepath=ojos_file
        )

        print(
            "RESULTADO LOAD_CLOTHES OJOS:",
            resultado
        )

        if "FINISHED" not in resultado:

            print(
                "ERROR: MPFB no pudo cargar "
                "los ojos."
            )

            return False

        ojos = bpy.data.objects.get(
            "Human.high-poly"
        )

        if not ojos:

            candidatos = [
                obj
                for obj in bpy.context.scene.objects
                if obj.name.startswith(
                    "Human.high-poly"
                )
            ]

            if candidatos:

                ojos = candidatos[-1]

        if not ojos:

            print(
                "ERROR: Los ojos fueron cargados "
                "pero no se encontró el objeto."
            )

            return False

        print(
            "OJOS CREADOS:",
            ojos.name
        )

        # ----------------------------------------------------
        # Aplicar textura MPFB
        # ----------------------------------------------------

        textura_ok = aplicar_textura_ojos(
            ojos
        )

        if textura_ok:

            print(
                "COLOR DE OJOS APLICADO:",
                OJOS
            )

        else:

            print(
                "AVISO: Los ojos fueron creados, "
                "pero no se pudo aplicar su textura."
            )

        return ojos

    except Exception as error:

        print(
            "ERROR APLICANDO OJOS:",
            error
        )

        return False


# ============================================================
# ELIMINAR HUMAN ANTERIOR
# ============================================================

def eliminar_humano_anterior():

    objetos_a_eliminar = [
        obj
        for obj in bpy.data.objects
        if obj.name.startswith(
            "Human"
        )
    ]

    for obj in objetos_a_eliminar:

        bpy.data.objects.remove(
            obj,
            do_unlink=True
        )

    print(
        "Avatar anterior eliminado."
    )


# ============================================================
# FONDO DE ESTUDIO
# ============================================================

def crear_fondo_estudio():

    """
    Crea un fondo sencillo y oscuro
    en Blender.
    """

    for obj in list(
        bpy.data.objects
    ):

        if obj.name.startswith(
            "VirtualFit_"
        ):

            bpy.data.objects.remove(
                obj,
                do_unlink=True
            )

    # --------------------------------------------------------
    # Piso
    # --------------------------------------------------------

    bpy.ops.mesh.primitive_plane_add(
        size=12,
        location=(0, 0, 0)
    )

    piso = bpy.context.object

    piso.name = (
        "VirtualFit_Floor"
    )

    mat = bpy.data.materials.get(
        "VirtualFit_Studio_Material"
    )

    if not mat:

        mat = bpy.data.materials.new(
            "VirtualFit_Studio_Material"
        )

    mat.diffuse_color = (
        0.055,
        0.065,
        0.08,
        1.0
    )

    mat.use_nodes = True

    bsdf = next(
        n
        for n in mat.node_tree.nodes
        if n.type == "BSDF_PRINCIPLED"
    )

    bsdf.inputs[
        "Base Color"
    ].default_value = (
        0.055,
        0.065,
        0.08,
        1.0
    )

    bsdf.inputs[
        "Roughness"
    ].default_value = 0.72

    piso.data.materials.append(
        mat
    )

    # --------------------------------------------------------
    # Pared
    # --------------------------------------------------------

    bpy.ops.mesh.primitive_plane_add(
        size=12,
        location=(0, 4.5, 5)
    )

    pared = bpy.context.object

    pared.name = (
        "VirtualFit_Backdrop"
    )

    pared.rotation_euler[0] = (
        1.5708
    )

    pared.data.materials.append(
        mat
    )

    # --------------------------------------------------------
    # Luces
    # --------------------------------------------------------

    for nombre, loc, energy, size in [

        (
            "VirtualFit_Key",
            (3.5, -3.5, 5.5),
            900,
            3.0
        ),

        (
            "VirtualFit_Fill",
            (-3.5, -1.5, 3.5),
            650,
            2.5
        ),

        (
            "VirtualFit_Rim",
            (0, 3.0, 4.5),
            850,
            2.0
        ),

    ]:

        data = bpy.data.lights.new(
            nombre,
            type="AREA"
        )

        data.energy = energy

        data.shape = "DISK"

        data.size = size

        obj = bpy.data.objects.new(
            nombre,
            data
        )

        bpy.context.collection.objects.link(
            obj
        )

        obj.location = loc

        direction = (
            Vector(
                (0, 0, 1.7)
            )
            - obj.location
        )

        if direction.length > 0:

            obj.rotation_euler = (
                direction
                .to_track_quat(
                    "-Z",
                    "Y"
                )
                .to_euler()
            )

    # --------------------------------------------------------
    # Mundo
    # --------------------------------------------------------

    world = (
        bpy.context.scene.world
    )

    if world is None:

        world = bpy.data.worlds.new(
            "VirtualFit_World"
        )

        bpy.context.scene.world = world

    world.use_nodes = True

    bg = (
        world.node_tree.nodes.get(
            "Background"
        )
    )

    if bg:

        bg.inputs[
            "Color"
        ].default_value = (
            0.025,
            0.03,
            0.04,
            1.0
        )

        bg.inputs[
            "Strength"
        ].default_value = 0.25

    print(
        "Fondo de estudio VirtualFit creado."
    )


# ============================================================
# CREAR AVATAR
# ============================================================

def crear_avatar():

    print(
        "================================"
    )

    print(
        "CREANDO AVATAR VIRTUALFIT"
    )

    print(
        "================================"
    )

    eliminar_humano_anterior()

    scene = bpy.context.scene

    # --------------------------------------------------------
    # CONFIGURAR MPFB
    # --------------------------------------------------------

    try:

        scene.MPFB_NH_phenotype_gender = (
            GENERO
        )

        scene.MPFB_NH_phenotype_age = (
            EDAD
        )

        scene.MPFB_NH_phenotype_height = (
            ALTURA
        )

        scene.MPFB_NH_phenotype_weight = (
            PESO
        )

        scene.MPFB_NH_phenotype_muscle = (
            MUSCULO
        )

        scene.MPFB_NH_phenotype_proportions = (
            PROPORCIONES
        )

    except Exception as error:

        print(
            "ERROR configurando MPFB:",
            error
        )

        return None

    # --------------------------------------------------------
    # CONFIGURAR ASSET LIBRARY
    # --------------------------------------------------------

    configurar_asset_library()

    # --------------------------------------------------------
    # CREAR HUMAN
    # --------------------------------------------------------

    try:

        bpy.ops.mpfb.create_human()

    except Exception as error:

        print(
            "ERROR creando humano:",
            error
        )

        return None

    # --------------------------------------------------------
    # DEBUG
    # --------------------------------------------------------

    print(
        "OBJETOS MPFB:",
        [
            (o.name, o.type)
            for o in bpy.context.scene.objects
        ]
    )

    avatar_debug = (
        bpy.data.objects.get(
            "Human"
        )
    )

    if avatar_debug:

        print(
            "DEBUG MATERIAL SLOTS HUMAN:",
            [
                m.name if m else None
                for m in avatar_debug.data.materials
            ]
        )

        print(
            "DEBUG POLIGONOS HUMAN:",
            len(
                avatar_debug.data.polygons
            )
        )

        print(
            "DEBUG INDICES MATERIAL:",
            sorted(
                set(
                    p.material_index
                    for p in avatar_debug.data.polygons
                )
            )
        )

        print(
            "DEBUG VERTEX GROUPS:",
            [
                g.name
                for g in avatar_debug.vertex_groups
            ]
        )

    # --------------------------------------------------------
    # PIEL
    # --------------------------------------------------------

    if preparar_material_piel():

        aplicar_apariencia()

    else:

        print(
            "AVISO: No se pudo preparar "
            "el material de piel."
        )

    # --------------------------------------------------------
    # CABELLO
    # --------------------------------------------------------

    cabello = preparar_cabello()

    if cabello:

        print(
            "CABELLO APLICADO CORRECTAMENTE"
        )

    else:

        print(
            "AVISO: No se pudo aplicar cabello."
        )

    # --------------------------------------------------------
    # OJOS
    # --------------------------------------------------------

    ojos = preparar_ojos()

    if ojos:

        print(
            "OJOS APLICADOS CORRECTAMENTE"
        )

    else:

        print(
            "AVISO: No se pudieron aplicar ojos."
        )

    # --------------------------------------------------------
    # FONDO
    # --------------------------------------------------------

    crear_fondo_estudio()

    print(
        "================================"
    )

    print(
        "AVATAR CREADO"
    )

    print(
        "================================"
    )

    print(
        "Genero:",
        GENERO
    )

    print(
        "Edad:",
        EDAD
    )

    print(
        "Altura:",
        ALTURA
    )

    print(
        "Peso:",
        PESO
    )

    print(
        "Musculo:",
        MUSCULO
    )

    print(
        "Proporciones:",
        PROPORCIONES
    )

    print(
        "Piel:",
        PIEL
    )

    print(
        "Ojos:",
        OJOS,
        "-",
        OJOS_DISPONIBLES[OJOS]
    )

    print(
        "Cabello:",
        CABELLO,
        "-",
        CABELLOS_DISPONIBLES[CABELLO]
    )

    print(
        "Color cabello:",
        COLOR_CABELLO
    )

    print(
        "================================"
    )

    return True


# ============================================================
# SELECCIONAR AVATAR
# ============================================================

def seleccionar_avatar():

    bpy.ops.object.select_all(
        action="DESELECT"
    )

    objetos_avatar = []

    human = bpy.data.objects.get(
        "Human"
    )

    if human:

        objetos_avatar.append(
            human
        )

    # --------------------------------------------------------
    # Objetos relacionados con Human
    # --------------------------------------------------------

    for obj in bpy.context.scene.objects:

        if obj == human:
            continue

        incluir = False

        if obj.name.startswith(
            "Human."
        ):

            incluir = True

        if obj.parent == human:

            incluir = True

        if (
            hasattr(obj, "parent")
            and obj.parent
            and obj.parent.name.startswith(
                "Human"
            )
        ):

            incluir = True

        if incluir:

            if obj not in objetos_avatar:

                objetos_avatar.append(
                    obj
                )

    if not objetos_avatar:

        raise RuntimeError(
            "No se encontró ningún objeto Human."
        )

    for obj in objetos_avatar:

        obj.select_set(
            True
        )

    bpy.context.view_layer.objects.active = (
        human
        if human
        else objetos_avatar[0]
    )

    print(
        "OBJETOS SELECCIONADOS PARA GLB:"
    )

    for obj in objetos_avatar:

        print(
            " -",
            obj.name,
            obj.type
        )

    return objetos_avatar


# ============================================================
# EXPORTAR GLB
# ============================================================

def exportar_glb():

    print(
        "================================"
    )

    print(
        "EXPORTANDO AVATAR"
    )

    print(
        "================================"
    )

    objetos_avatar = (
        seleccionar_avatar()
    )

    bpy.ops.object.select_all(
        action="DESELECT"
    )

    for obj in objetos_avatar:

        obj.select_set(
            True
        )

    human = bpy.data.objects.get(
        "Human"
    )

    if human:

        bpy.context.view_layer.objects.active = (
            human
        )

    # --------------------------------------------------------
    # Empaquetar texturas
    # --------------------------------------------------------

    try:

        bpy.ops.file.pack_all()

        print(
            "RECURSOS EMPAQUETADOS EN BLENDER."
        )

    except Exception as error:

        print(
            "AVISO empaquetando recursos:",
            error
        )

    # --------------------------------------------------------
    # DEBUG HUMAN
    # --------------------------------------------------------

    avatar = bpy.data.objects.get(
        "Human"
    )

    if avatar:

        print(
            "========== MATERIALES HUMAN =========="
        )

        print(
            "SLOTS:",
            [
                m.name if m else None
                for m in avatar.data.materials
            ]
        )

        conteo_materiales = {}

        for p in avatar.data.polygons:

            idx = p.material_index

            if (
                idx
                < len(
                    avatar.data.materials
                )
            ):

                material = (
                    avatar.data.materials[
                        idx
                    ]
                )

                nombre = (
                    material.name
                    if material
                    else "SIN_MATERIAL"
                )

            else:

                nombre = (
                    "SIN_MATERIAL"
                )

            conteo_materiales[
                nombre
            ] = (
                conteo_materiales.get(
                    nombre,
                    0
                )
                + 1
            )

        print(
            "POLIGONOS POR MATERIAL:",
            conteo_materiales
        )

        print(
            "======================================"
        )

    # --------------------------------------------------------
    # EXPORTACIÓN GLB
    # --------------------------------------------------------

    try:

        bpy.ops.export_scene.gltf(

            filepath=OUTPUT_FILE,

            export_format="GLB",

            use_selection=True,

            export_apply=True,

            export_animations=True,

            export_skins=True,

            export_morph=True,

        )

    except Exception as error:

        print(
            "ERROR EXPORTANDO GLB:",
            error
        )

        return False

    print(
        "================================"
    )

    print(
        "GLB EXPORTADO CORRECTAMENTE:"
    )

    print(
        OUTPUT_FILE
    )

    print(
        "================================"
    )

    return True


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

argumentos()

validar_opciones()

resultado = crear_avatar()

if resultado:

    exportar_glb()

else:

    print(
        "NO SE PUDO CREAR EL AVATAR"
    )