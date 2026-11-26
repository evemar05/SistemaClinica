using Clinica.Ayudas;
using Clinica.Models;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

namespace Clinica.Controllers
{
    public class FacturacionController : Controller
    {
        public IActionResult Index()
        {
            SocketPagina socket = new SocketPagina();
            string json = "{\"accion\":\"listar_facturas\"}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaFacturas facturas = JsonSerializer.Deserialize<RespuestaFacturas>(respuesta);

            return View(facturas.datos);
        }

        [HttpGet]
        public IActionResult Buscar()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Buscar(int idCita)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""buscar_cita"",""idCita"":{idCita}}}";
            string respuesta = socket.EnviarPeticion(json);
            RespuestaCita resultado = JsonSerializer.Deserialize<RespuestaCita>(respuesta);

            if (resultado.estatus != 0)
            {
                ViewBag.Error = resultado.mensaje;
                return View();
            }

            string jsonFactura = $@"{{""accion"":""buscar_factura_cita"",""idCita"":{idCita}}}";
            string respuestaFactura = socket.EnviarPeticion(jsonFactura);
            RespuestaFactura factura = JsonSerializer.Deserialize<RespuestaFactura>(respuestaFactura);

            if (factura.estatus == 0)
            {
                return View("YaFacturada", factura.datos);
            }

            return RedirectToAction("Registrar", new { idCita = resultado.datos.idCita });
        }

        [HttpGet]
        public IActionResult Registrar(int idCita)
        {
            var factura = new FacturaModel { idCita = idCita };
            return View(factura);
        }

        [HttpPost]
        public IActionResult Registrar(FacturaModel factura)
        {
            const decimal PORCENTAJE_IVA = 0.13m;
            factura.iva = Math.Round(factura.precio * PORCENTAJE_IVA, 2);
            factura.total = factura.precio + factura.iva;
            return View("Confirmar", factura);
        }

        [HttpPost]
        public IActionResult Confirmar(FacturaModel factura)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""crear_factura"",
                ""idCita"":{factura.idCita},
                ""servicio"":""{factura.servicio}"",
                ""precio"":{factura.precio.ToString(System.Globalization.CultureInfo.InvariantCulture)}
            }}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaFactura resultado = JsonSerializer.Deserialize<RespuestaFactura>(respuesta);

            if (resultado.estatus != 0)
            {
                ViewBag.Error = resultado.mensaje;
                return View("Registrar", factura);
            }

            return RedirectToAction("Index");
        }
    }
}
