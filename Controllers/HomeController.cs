using Clinica.Models;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;


namespace Clinica.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index()
        {

            return View();
        }

    }
}
