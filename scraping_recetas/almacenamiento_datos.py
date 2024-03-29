# coding=utf-8
import django
import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parent.parent.__str__())
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','scraping_recetas.locale_settings')

django.setup()
from extraccion_datos import get_datos
from scraping_recetas_app.models import Receta, Categoria, IngredienteReceta, PreparacionReceta, Subcategoria
from django.db import transaction


@transaction.atomic
def almacena_datos():
    """
    Este método consulta los datos de las recetas para almacenarlos en la base de datos mediante los modelos
    creados en Django. Lo trataremos como una transacción atómica, es decir, sólo guardaremos todos los cambios en la BD
    si se han podido guardar correctamente TODAS las recetas.
    """
    sid = transaction.savepoint()
    datos = get_datos()
    print("Iniciando extracción...")
    for categoria, subcategoria in datos.items():
        print("Guardando categoría: " + categoria)
        try:
            c = Categoria(nombre=categoria)
            c.save()
        except Exception as e:
            # En caso que haya alguna excepción al guardar, escribimos el mensaje en la consola y deshacemos los cambios
            # en la BD
            print(str(e))
            transaction.savepoint_rollback(sid)
            break

        for sub, recetas in subcategoria.items():
            print("Guardando subcategoría: " + sub)
            try:
                s = Subcategoria(nombre=sub, categoria=c)
                s.save()
            except Exception as e:
                # En caso que haya alguna excepción al guardar, escribimos el mensaje en la consola y deshacemos los cambios
                # en la BD
                print(str(e))
                
                transaction.savepoint_rollback(sid)
                break
            
            for r in recetas:
                titulo = r.get("titulo")
                tipo_comida = r.get("tipo_comida")
                comensales = r.get("comensales")
                duracion = r.get("duracion")
                ingredientes = r.get("ingredientes")
                descripcion = r.get("descripcion")
                prepacacion = r.get("preparacion")
                try:
                    rec = Receta(titulo=titulo, tipo_comida=tipo_comida, comensales=comensales, duracion=duracion,
                                descripcion=descripcion, subcategoria=s)
                    rec.save()
                except Exception as e:
                    # En caso que haya alguna excepción al guardar, escribimos el mensaje en la consola y deshacemos los cambios
                    # en la BD
                    print(str(e))
                    transaction.savepoint_rollback(sid)
                    break

                for i in ingredientes:
                    try:
                        IngredienteReceta(receta=rec, ingrediente=i).save()
                    except Exception as e:
                        # En caso que haya alguna excepción al guardar, escribimos el mensaje en la consola y deshacemos los cambios
                        # en la BD
                        print(str(e))
                        transaction.savepoint_rollback(sid)
                        break

                for p in prepacacion:
                    try:
                        PreparacionReceta(receta=rec, orden=p.get("orden"), descripcion=p.get("descripcion")).save()
                    except Exception as e:
                        # En caso que haya alguna excepción al guardar, escribimos el mensaje en la consola y deshacemos los cambios
                        # en la BD
                        print(str(e))
                        transaction.savepoint_rollback(sid)
                        break

    print("Guardado con éxito.")


if __name__ == "__main__":
    almacena_datos()
