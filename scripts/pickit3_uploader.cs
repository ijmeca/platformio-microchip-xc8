using System;
using System.IO;
using System.Reflection;
using System.Threading;
using System.Windows.Forms;

internal static class PICkit3Uploader
{
    [STAThread]
    private static int Main(string[] args)
    {
        try
        {
            string application = Argument(args, "--application");
            string deviceFile = Argument(args, "--device-file");
            string expectedDevice = NormalizeDevice(Argument(args, "--device"));
            string hexFile = Argument(args, "--hex");

            if (!File.Exists(application) || !File.Exists(deviceFile) || !File.Exists(hexFile))
                throw new FileNotFoundException("PICkit 3 application, device file, or HEX not found.");

            Environment.CurrentDirectory = Path.GetDirectoryName(application);
            Assembly api = Assembly.LoadFile(Path.GetFullPath(application));
            Type formType = RequireType(api, "PICkit2V2.FormPICkit2");
            Type functionsType = RequireType(api, "PICkit2V2.PICkitFunctions");
            Type importType = RequireType(api, "PICkit2V2.ImportExportHex");

            formType.GetField("DeviceFileName", BindingFlags.Public | BindingFlags.Static)
                .SetValue(null, Path.GetFullPath(deviceFile));
            formType.GetField("ShowWriteEraseVDDDialog", BindingFlags.Public | BindingFlags.Static)
                .SetValue(null, false);

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            using (Form form = (Form)Activator.CreateInstance(formType))
            {
                form.ShowInTaskbar = false;
                form.Opacity = 0;
                form.Show();
                for (int attempt = 0; attempt < 20; attempt++)
                {
                    Application.DoEvents();
                    if (ActiveDeviceName(functionsType).Length != 0)
                        break;
                    Thread.Sleep(100);
                }
                form.Hide();

                string detectedDevice = ActiveDeviceName(functionsType);
                if (detectedDevice.Length == 0)
                    throw new InvalidOperationException("No target device detected by PICkit 3.");
                if (!String.Equals(detectedDevice, expectedDevice, StringComparison.OrdinalIgnoreCase))
                    throw new InvalidOperationException(
                        "Detected device " + detectedDevice + ", expected " + expectedDevice + ".");

                object importResult = importType.GetMethod(
                    "ImportHexFile", BindingFlags.Public | BindingFlags.Static)
                    .Invoke(null, new object[] { Path.GetFullPath(hexFile), true, true });
                if (Convert.ToInt32(importResult) != 0)
                    throw new InvalidOperationException("PICkit 3 rejected the HEX file: " + importResult);

                Console.WriteLine("PICkit 3 detected: " + detectedDevice);
                Console.WriteLine("Programming and verifying: " + Path.GetFullPath(hexFile));
                bool success = (bool)formType.GetMethod("ExtCallWrite", BindingFlags.Public | BindingFlags.Instance)
                    .Invoke(form, new object[] { true });
                if (!success)
                    throw new InvalidOperationException("PICkit 3 programming or verification failed.");
            }

            Console.WriteLine("PICkit 3 programming successful.");
            return 0;
        }
        catch (TargetInvocationException error)
        {
            Console.Error.WriteLine(error.InnerException != null ? error.InnerException.Message : error.Message);
            return 1;
        }
        catch (Exception error)
        {
            Console.Error.WriteLine(error.Message);
            return 1;
        }
    }

    private static string ActiveDeviceName(Type functionsType)
    {
        int activePart = (int)functionsType.GetField("ActivePart", BindingFlags.Public | BindingFlags.Static)
            .GetValue(null);
        object deviceFile = functionsType.GetField("DevFile", BindingFlags.Public | BindingFlags.Static)
            .GetValue(null);
        if (deviceFile == null || activePart <= 0)
            return "";
        Array parts = (Array)deviceFile.GetType().GetField("PartsList").GetValue(deviceFile);
        object part = parts.GetValue(activePart);
        FieldInfo name = part.GetType().GetField("PartName");
        return NormalizeDevice(Convert.ToString(name.GetValue(part)));
    }

    private static Type RequireType(Assembly assembly, string name)
    {
        Type type = assembly.GetType(name, false);
        if (type == null)
            throw new InvalidOperationException("Unsupported PICkit 3 application API: " + name);
        return type;
    }

    private static string NormalizeDevice(string value)
    {
        string device = value.Trim().ToUpperInvariant();
        return device.StartsWith("PIC") ? device.Substring(3) : device;
    }

    private static string Argument(string[] args, string name)
    {
        for (int index = 0; index + 1 < args.Length; index++)
            if (args[index] == name)
                return args[index + 1];
        throw new ArgumentException("Missing required argument " + name + ".");
    }
}
