using Microsoft.AspNetCore.Mvc;

namespace Clinica.Controllers
{
    public class MenuController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
